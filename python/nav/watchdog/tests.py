#
# Copyright (C) 2014 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.  You should have received a copy of the GNU General Public
# License along with NAV. If not, see <http://www.gnu.org/licenses/>.
#
"""Test classes for WatchDog"""

import collections
import itertools
from datetime import datetime, timedelta
from django.utils.timesince import timesince

from nav.asyncdns import reverse_lookup
from nav.models.manage import IpdevpollJobLog, Netbox, Arp, Cam


STATUS_OK = 'ok'
STATUS_NOT_OK = 'not_ok'
STATUS_UNKNOWN = 'unknown'


class TestResult(object):
    """Result for test errors"""

    def __init__(self, description, obj=None):
        self.description = description  # The human readable description
        self.obj = obj  # An optional object representing the test

    def __unicode__(self):
        return unicode(self.description)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Test(object):
    """Interface for all test classes"""

    name = 'Test'
    description = 'A WatchDog test'

    def __init__(self):
        self.status = STATUS_UNKNOWN
        self.errors = []

    def _get_errors(self):
        """Gets error list for this test"""
        raise NotImplementedError

    def run(self):
        """Runs the test. Sets self.errors and self.status"""
        self.errors = self._get_errors()
        self.status = (STATUS_OK if len(self.errors) == 0
                       else STATUS_NOT_OK)

    def get_status(self):
        """Runs the test and returns status"""
        self.run()
        return self.status


class TestOverdueJobs(Test):
    """Tests if there are any overdue ipdevpoll jobs"""

    name = 'Job duration'
    description = 'Tests if there exists any overdue ipdevpoll jobs'

    def _get_errors(self):
        """
        Fetches the overdue jobs from ipdevpolljoblog. Because some jobs will
        take some time to run, give some slack to what is considered overdue.
        """
        slack = 120  # Seconds

        query = """
          SELECT ijl.* FROM ipdevpoll_job_log AS ijl
          JOIN
          (
            SELECT netboxid, job_name, MAX(end_time) AS end_time
            FROM ipdevpoll_job_log
            GROUP BY netboxid, job_name
          ) AS foo
          USING (netboxid, job_name, end_time)
          JOIN netbox ON (ijl.netboxid = netbox.netboxid)
          WHERE now() - interval '1 second' * interval > end_time
          ORDER BY netboxid;
        """

        errors = []
        for job in IpdevpollJobLog.objects.raw(query):
            should_have_run = job.end_time + timedelta(seconds=job.interval)
            overdue_by = datetime.now() - should_have_run
            if overdue_by.seconds > slack:
                time_since = timesince(datetime.now() - overdue_by)
                descr = "Job {} on {} is overdue by {}".format(
                    job.job_name, job.netbox.sysname, time_since)
                errors.append(TestResult(descr, job))

        return errors


class TestFailedJobs(Test):
    """Tests if there are any ipdevpolljobs that have failed"""

    name = 'Job status'
    description = 'Tests if there are any ipdevpoll jobs that repeatedly fails'

    def _get_errors(self):
        """Fetches failed ipdevpoll jobs"""
        query = """
          SELECT ijl.* FROM ipdevpoll_job_log AS ijl
          JOIN
          (
            SELECT netboxid, job_name, MAX(end_time) AS end_time
            FROM ipdevpoll_job_log
            GROUP BY netboxid, job_name
          ) AS foo
          USING (netboxid, job_name, end_time)
          JOIN netbox ON (ijl.netboxid = netbox.netboxid)
          WHERE success = 'f'
          ORDER BY netboxid;
        """

        results = []
        fail_count = 3  # Number of successive failed jobs that equals problem
        for failed in IpdevpollJobLog.objects.raw(query):
            last_jobs = IpdevpollJobLog.objects.filter(
                netbox=failed.netbox, job_name=failed.job_name)\
                .order_by('end_time')[0:fail_count]
            if all([not job.success for job in last_jobs]):
                descr = "Job {} on {} has failed the last {} times.".format(
                    failed.job_name, failed.netbox, fail_count)
                results.append(TestResult(descr, failed))

        return results


class TestDuplicateHostnameForIP(Test):
    """
    Tests of there are any number of IP-addresses that resolve to the same
    hostname
    """

    name = 'Hostname sanity'
    description = 'Tests if there are IP-addresses that resolve to the ' \
                  'same hostname'

    def _get_errors(self):
        """Fetches duplicate hostnames"""
        ip_addresses = [n.ip for n in Netbox.objects.all()]
        reverse_names = reverse_lookup(ip_addresses)
        flatten = list(itertools.chain(*reverse_names.values()))
        duplicates = set([x for x in flatten if flatten.count(x) > 1])
        results = collections.defaultdict(list)

        for hostname in duplicates:
            for ip, hostlist in reverse_names.items():
                if hostname in hostlist:
                    results[hostname].append(ip)

        errors = []
        for hostname, iplist in results.items():
            error = 'The hostname {} is used by these IP-addresses: {}'.format(
                hostname, ', '.join(iplist))
            errors.append(TestResult(error))

        return errors


class TestNoRouterInterfaces(Test):
    """Test if any router has no router-interfaces"""

    name = 'Router interface count'
    description = 'Tests if there are routers that do not have any router ' \
                  'interfaces'

    def _get_errors(self):
        """Fetches routers with no router interfaces"""
        results = []
        for netbox in Netbox.objects.filter(category__in=['GW', 'GSW']):
            if netbox.get_gwports().count() <= 0:
                descr = "{} has no router-interfaces".format(netbox.sysname)
                results.append(TestResult(descr, netbox))

        return results


class TestNoSwitchPorts(Test):
    """Test if any switch has no switch ports"""

    name = 'Switch port count'
    description = 'Tests if there are any switches that do not have any ' \
                  'switch ports'

    def _get_errors(self):
        """Fetches switches with no switch ports"""
        results = []
        for netbox in Netbox.objects.filter(category__in=['GSW', 'SW']):
            if netbox.get_swports().count() <= 0:
                descr = "{} has no switch ports".format(netbox.sysname)
                results.append(TestResult(descr, netbox))

        return results


class TestAbnormalInterfaceCount(Test):
    """Tests for abnormal interface counts on devices"""

    # Random number, should be sanitized. Max for a Cisco 7200 with
    # 12.3T software is 20000. 5000 is above most of the other though.
    # But what is the case where this test is needed?
    abnormal_amount = 5000
    name = 'Total interface count'
    description = 'Tests if there are IP Devices with more than {} ' \
        'interfaces'.format(abnormal_amount)

    def _get_errors(self):
        """Fetches netboxes with an abnormal amount of interfaces"""
        results = []
        for netbox in Netbox.objects.all().order_by('sysname'):
            count = netbox.interface_set.count()
            if count > self.abnormal_amount:
                descr = "{} has {} interfaces".format(netbox.sysname, count)
                results.append(TestResult(descr, netbox))

        return results


class TestNewCamAndArpRecords(Test):
    """Tests for new Arp and Cam records"""

    slack = 60 * 60  # 1 hour in seconds
    name = "ARP and CAM"
    description = "Tests if ARP and CAM has been collected the last hour"

    def _get_errors(self):
        """Checks for latest cam and arp"""
        results = []

        arp_result = self.test_arp()
        if arp_result:
            results.append(arp_result)
        cam_result = self.test_cam()
        if cam_result:
            results.append(cam_result)

        return results

    def test_cam(self):
        """Test latest CAM record"""
        now = datetime.now()
        recently = timedelta(seconds=self.slack)
        latest_cam = self.get_latest(Cam)
        if latest_cam:
            cam_diff = now - latest_cam.start_time
            if cam_diff > recently:
                descr = 'CAM-records has not been collected ' \
                        'the last {}'.format(timesince(latest_cam.start_time))
                return TestResult(descr, latest_cam)

    def test_arp(self):
        """Test latest ARP record"""
        now = datetime.now()
        recently = timedelta(seconds=self.slack)
        latest_arp = self.get_latest(Arp)
        if latest_arp:
            arp_diff = now - latest_arp.start_time
            if arp_diff > recently:
                descr = 'ARP-records has not been collected the ' \
                        'last {}'.format(timesince(latest_arp.start_time))
                return TestResult(descr, latest_arp)

    @staticmethod
    def get_latest(thing):
        """Get latest Cam or Arp record"""
        try:
            latest = thing.objects.all().order_by('-start_time')[0]
        except IndexError:
            return None
        else:
            return latest
