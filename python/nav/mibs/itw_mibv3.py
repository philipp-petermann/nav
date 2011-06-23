# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2011 UNINETT AS
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
import mibretriever

class ItWatchDogsMibV3(mibretriever.MibRetriever):
    from nav.smidumps.itw_mibv3 import MIB as mib

    def retrieve_std_columns(self):
        """ A convenient function for getting the most interesting
        columns for environment mibs. """

        return self.retrieve_columns([
                'climateName',
                'climateAvail',
                'climateTempC',
                'climateHumidity',
                'climateLight',
                'climateAirflow',
                'climateSound',
                'climateIO1',
                'climateIO2',
                'climateIO3',
                'climateDewPointC',
                'powMonName',
                'powMonAvail',
                'powMonKWattHrs',
                'powMonVolts',
                'powMonDeciAmps',
                'powMonRealPower',
                'powMonApparentPower',
                'powMonPowerFactor',
                'powMonOutlet1',
                'powMonOutlet2',
                'tempSensorName',
                'tempSensorAvail',
                'tempSensorTempC',
                'airFlowSensorName',
                'airFlowSensorAvail',
                'airFlowSensorTempC',
                'airFlowSensorFlow',
                'airFlowSensorHumidity',
                'airFlowSensorDewPointC',
                'powerName',
                'powerAvail',
                'powerVolts',
                'powerDeciAmps',
                'powerRealPower',
                'powerApparentPower',
                'powerApparentPower',
                'powerPowerFactor',
                'doorSensorName',
                'doorSensorAvail',
                'doorSensorStatus',
                'waterSensorName',
                'waterSensorAvail',
                'waterSensorDampness',
                'currentMonitorName',
                'currentMonitorAvail',
                'currentMonitorDeciAmps',
                'millivoltMonitorName',
                'millivoltMonitorAvail',
                'millivoltMonitorMV',
                'pow3ChName',
                'pow3ChAvail',
                'pow3ChKWattHrsA',
                'pow3ChVoltsA',
                'pow3ChDeciAmpsA'
                'pow3ChVoltMaxA',
                'pow3ChVoltMinA',
                'pow3ChVoltPeakA',
                'pow3ChDeciAmpsA',
                'pow3ChRealPowerA',
                'pow3ChApparentPowerA',
                'pow3ChPowerFactorA',
                'pow3ChKWattHrsB',
                'pow3ChVoltsB',
                'pow3ChVoltMaxB',
                'pow3ChVoltMinB',
                'pow3ChVoltPeakB',
                'pow3ChDeciAmpsB',
                'pow3ChRealPowerB',
                'pow3ChApparentPowerB',
                'pow3ChPowerFactorB',
                'pow3ChKWattHrsC',
                'pow3ChVoltsC',
                'pow3ChVoltMaxC',
                'pow3ChVoltMinC',
                'pow3ChVoltPeakC',
                'pow3ChDeciAmpsC',
                'pow3ChRealPowerC',
                'pow3ChApparentPowerC',
                'pow3ChPowerFactorC',
                'outletName',
                'outletAvail',
                'outlet1Status',
                'outlet2Status',
                'vsfcName',
                'vsfcAvail',
                'vsfcSetPointC',
                'vsfcFanSpeed',
                'vsfcIntTempC',
                'vsfcExt1TempC',
                'vsfcExt2TempC',
                'vsfcExt3TempC',
                'vsfcExt4TempC',
                'ctrl3ChName',
                'ctrl3ChAvail',
                'ctrl3ChVoltsA',
                'ctrl3ChVoltPeakA',
                'ctrl3ChDeciAmpsA',
                'ctrl3ChDeciAmpsPeakA',
                'ctrl3ChRealPowerA',
                'ctrl3ChApparentPowerA',
                'ctrl3ChPowerFactorA',
                'ctrl3ChVoltsB',
                'ctrl3ChVoltPeakB',
                'ctrl3ChDeciAmpsB',
                'ctrl3ChDeciAmpsPeakB',
                'ctrl3ChRealPowerB',
                'ctrl3ChApparentPowerB',
                'ctrl3ChPowerFactorB',
                'ctrl3ChVoltsC',
                'ctrl3ChVoltPeakC',
                'ctrl3ChDeciAmpsC',
                'ctrl3ChDeciAmpsPeakC',
                'ctrl3ChRealPowerC',
                'ctrl3ChApparentPowerC',
                'ctrl3ChPowerFactorC',
                'ctrlGrpAmpsName',
                'ctrlGrpAmpsAvail',
                'ctrlGrpAmpsA',
                'ctrlGrpAmpsB',
                'ctrlGrpAmpsC',
                'ctrlGrpAmpsD',
                'ctrlGrpAmpsE',
                'ctrlGrpAmpsF',
                'ctrlGrpAmpsG',
                'ctrlGrpAmpsH',
                'ctrlGrpAmpsAVolts',
                'ctrlGrpAmpsBVolts',
                'ctrlGrpAmpsCVolts',
                'ctrlGrpAmpsDVolts',
                'ctrlGrpAmpsEVolts',
                'ctrlGrpAmpsFVolts',
                'ctrlGrpAmpsGVolts',
                'ctrlGrpAmpsHVolts',
                'ctrlOutletName',
                'ctrlOutletStatus',
                'ctrlOutletFeedback',
                'ctrlOutletPending',
                'ctrlOutletDeciAmps',
                'ctrlOutletGroup',
                'ctrlOutletUpDelay',
                'ctrlOutletDwnDelay',
                'ctrlOutletRbtDelay',
                'ctrlOutletURL',
                'ctrlOutletPOAAction',
                'ctrlOutletPOADelay',
                'ctrlOutletKWattHrs',
                'ctrlOutletPower',
                'dewPointSensorName',
                'dewPointSensorAvail',
                'dewPointSensorTempC',
                'dewPointSensorHumidity',
                'dewPointSensorDewPointC',
                'digitalSensorName',
                'digitalSensorAvail',
                'digitalSensorDigital',
                'dstsName',
                'dstsAvail',
                'dstsVoltsA',
                'dstsDeciAmpsA',
                'dstsVoltsB',
                'dstsDeciAmpsB',
                'dstsSourceAActive',
                'dstsSourceBActive',
                'dstsPowerStatusA',
                'dstsPowerStatusB',
                'dstsSourceATempC',
                'dstsSourceBTempC',
                'cpmSensorName',
                'cpmSensorAvail',
                'cpmSensorStatus',
                'smokeAlarmName',
                'smokeAlarmAvail',
                'smokeAlarmStatus',
                'neg48VdcSensorName',
                'neg48VdcSensorAvail',
                'neg48VdcSensorVoltage',
                'pos30VdcSensorName',
                'pos30VdcSensorAvail',
                'pos30VdcSensorVoltage',
                'analogSensorName',
                'analogSensorAvail',
                'analogSensorAnalog',
                'ctrl3ChIECName',
                'ctrl3ChIECAvail',
                'ctrl3ChIECKWattHrsA',
                'ctrl3ChIECVoltsA',
                'ctrl3ChIECVoltPeakA',
                'ctrl3ChIECDeciAmpsA',
                'ctrl3ChIECDeciAmpsPeakA',
                'ctrl3ChIECRealPowerA',
                'ctrl3ChIECApparentPowerA',
                'ctrl3ChIECPowerFactorA',
                'ctrl3ChIECKWattHrsB',
                'ctrl3ChIECVoltsB',
                'ctrl3ChIECVoltPeakB',
                'ctrl3ChIECDeciAmpsB',
                'ctrl3ChIECDeciAmpsPeakB',
                'ctrl3ChIECRealPowerB',
                'ctrl3ChIECApparentPowerB',
                'ctrl3ChIECPowerFactorB',
                'ctrl3ChIECKWattHrsC',
                'ctrl3ChIECVoltsC',
                'ctrl3ChIECVoltPeakC',
                'ctrl3ChIECDeciAmpsC',
                'ctrl3ChIECDeciAmpsPeakC',
                'ctrl3ChIECRealPowerC',
                'ctrl3ChIECApparentPowerC',
                'ctrl3ChIECPowerFactorC',
                'climateRelayName',
                'climateRelayAvail',
                'climateRelayTempC',
                'climateRelayIO1',
                'climateRelayIO2',
                'climateRelayIO3',
                'climateRelayIO4',
                'climateRelayIO5',
                'climateRelayIO6',
                'ctrlRelayName',
                'ctrlRelayState',
                'ctrlRelayLatchingMode',
                'ctrlRelayOverride',
                'ctrlRelayAcknowledge',
                'airSpeedSwitchSensorName',
                'airSpeedSwitchSensorAvail',
                'airSpeedSwitchSensorAirSpeed',
                'powerDMName',
                'powerDMAvail',
                'powerDMUnitInfoTitle',
                'powerDMUnitInfoVersion',
                'powerDMUnitInfoMainCount',
                'powerDMUnitInfoAuxCount',
                'powerDMChannelName1',
                'powerDMChannelName2',
                'powerDMChannelName3',
                'powerDMChannelName4',
                'powerDMChannelName5',
                'powerDMChannelName6',
                'powerDMChannelName7',
                'powerDMChannelName8',
                'powerDMChannelName9',
                'powerDMChannelName10',
                'powerDMChannelName11',
                'powerDMChannelName12',
                'powerDMChannelName13',
                'powerDMChannelName14',
                'powerDMChannelName15',
                'powerDMChannelName16',
                'powerDMChannelName17',
                'powerDMChannelName18',
                'powerDMChannelName19',
                'powerDMChannelName20',
                'powerDMChannelName21',
                'powerDMChannelName22',
                'powerDMChannelName23',
                'powerDMChannelName24',
                'powerDMChannelName25',
                'powerDMChannelName26',
                'powerDMChannelName27',
                'powerDMChannelName28',
                'powerDMChannelName29',
                'powerDMChannelName30',
                'powerDMChannelName31',
                'powerDMChannelName32',
                'powerDMChannelName33',
                'powerDMChannelName34',
                'powerDMChannelName35',
                'powerDMChannelName36',
                'powerDMChannelName37',
                'powerDMChannelName38',
                'powerDMChannelName39',
                'powerDMChannelName40',
                'powerDMChannelName41',
                'powerDMChannelName42',
                'powerDMChannelName43',
                'powerDMChannelName44',
                'powerDMChannelName45',
                'powerDMChannelName46',
                'powerDMChannelName47',
                'powerDMChannelName48',
                'powerDMChannelFriendly1',
                'powerDMChannelFriendly2',
                'powerDMChannelFriendly3',
                'powerDMChannelFriendly4',
                'powerDMChannelFriendly5',
                'powerDMChannelFriendly6',
                'powerDMChannelFriendly7',
                'powerDMChannelFriendly8',
                'powerDMChannelFriendly9',
                'powerDMChannelFriendly10',
                'powerDMChannelFriendly11',
                'powerDMChannelFriendly12',
                'powerDMChannelFriendly13',
                'powerDMChannelFriendly14',
                'powerDMChannelFriendly15',
                'powerDMChannelFriendly16',
                'powerDMChannelFriendly17',
                'powerDMChannelFriendly18',
                'powerDMChannelFriendly19',
                'powerDMChannelFriendly20',
                'powerDMChannelFriendly21',
                'powerDMChannelFriendly22',
                'powerDMChannelFriendly23',
                'powerDMChannelFriendly24',
                'powerDMChannelFriendly25',
                'powerDMChannelFriendly26',
                'powerDMChannelFriendly27',
                'powerDMChannelFriendly28',
                'powerDMChannelFriendly29',
                'powerDMChannelFriendly30',
                'powerDMChannelFriendly31',
                'powerDMChannelFriendly32',
                'powerDMChannelFriendly33',
                'powerDMChannelFriendly34',
                'powerDMChannelFriendly35',
                'powerDMChannelFriendly36',
                'powerDMChannelFriendly37',
                'powerDMChannelFriendly38',
                'powerDMChannelFriendly38',
                'powerDMChannelFriendly40',
                'powerDMChannelFriendly41',
                'powerDMChannelFriendly42',
                'powerDMChannelFriendly43',
                'powerDMChannelFriendly44',
                'powerDMChannelFriendly45',
                'powerDMChannelFriendly46',
                'powerDMChannelFriendly47',
                'powerDMChannelFriendly48',
                ])

    def get_module_name(self):
        return self.mib.get('moduleName', None)

    def get_sensor_descriptions(self, res):
        return []
