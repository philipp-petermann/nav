# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2011 UNINETT AS
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
"""ipdevpoll plugin to collect bridge data.

This plugin doesn't do much except find baseport numbers for switch
ports, using the BRIDGE-MIB.  The plugin also supports multiple
BRIDGE-MIB instances if they are listed as logical entities in
ENTITY-MIB.

"""

from nav.mibs.bridge_mib import BridgeMib
from nav.mibs.entity_mib import EntityMib
from nav.ipdevpoll import Plugin
from nav.ipdevpoll import shadows
from nav.ipdevpoll.utils import fire_eventually

class Bridge(Plugin):
    @classmethod
    def can_handle(cls, netbox):
        return True

    def handle(self):
        self._logger.debug("Collecting bridge data")
        self.entity = EntityMib(self.agent)
        self.bridgemib = BridgeMib(self.agent)
        self.baseports = {}

        df = self.entity.retrieve_alternate_bridge_mibs()
        df.addCallback(self._prune_bridge_mib_list)
        df.addCallback(self._query_baseports)

        return df

    def _prune_bridge_mib_list(self, result):
        """Prune the list of alternate bridge mib instances.

        Any instance with a previously known community is removed from
        the result list.

        """
        self._logger.debug("Alternate BRIDGE-MIB instances: %r", result)

        seen_communities = set(self.agent.community)
        new_result = []

        for descr, community in result:
            if community not in seen_communities:
                new_result.append((descr, community))
                seen_communities.add(community)

        return new_result
        

    def _query_baseports(self, bridgemibs):
        """Set up a chain to query each of the known BRIDGE-MIB instances."""

        self._logger.debug("Querying the following alternative instances: %r",
                          [b[0] for b in bridgemibs])

        # Set up a bunch of instances to poll
        instances = [ (None, self.agent.community) ] + bridgemibs

        instances = iter(instances)
        df = self._query_next_instance(None, instances)
        return df

    def _query_next_instance(self, result, instances):
        """Callback to be chained for each BRIDGE-MIB instance to query.

        This callback does the actual retrieval of the baseport list
        for a single BRIDGE-MIB instance, adds the intermediate
        results to the final set of baseports, and chains itself to
        collect from the next instance.

        """
        # Append any new result to the set of existing results
        if result:
            if not self.baseports:
                self.baseports = result
            else:
                self.baseports.update(result)

        try:
            descr, instance_community = instances.next()
        except StopIteration:
            return self._set_port_numbers(self.baseports)

        # Add the next bridge mib instance to the chain
        (self.agent.community, original_community) = (instance_community,
                                                      self.agent.community)
        def _reset_community(result):
            self.agent.community = original_community
            return result

        def _log_count(result):
            self._logger.debug("found %d switch ports on %r",
                               len(result), descr)
            return result

        df = self.bridgemib.retrieve_column('dot1dBasePortIfIndex')
        df.addBoth(_reset_community)
        df.addCallback(_log_count)
        df.addCallback(self._query_next_instance, instances)
        df.addCallback(lambda thing: fire_eventually(thing))
        return df

    def _set_port_numbers(self, result):
        """Process the list of collected base ports and set port numbers."""

        self._logger.debug("found a total of %d unique switch ports: %r",
                           len(result),
                           [portnum[0] for portnum in result.keys()])

        # Now save stuff to containers and pass the list of containers
        # to the next callback
        for portnum, ifindex in result.items():
            # The index is a single integer
            portnum = portnum[0]
            interface = self.containers.factory(ifindex, shadows.Interface)
            interface.baseport = portnum

        return result
    
