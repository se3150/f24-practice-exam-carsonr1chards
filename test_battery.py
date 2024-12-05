import pytest
from battery import Battery
from unittest.mock import Mock

todo = pytest.mark.skip(reason='todo: pending spec')

@pytest.fixture
def charged_battery():
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 70
    return b


def describe_Battery():

    def describe_init():

        def it_sets_charge_and_capacity():
            b = Battery(100)
            assert b.mCharge == 100
            assert b.mCapacity == 100

    def describe_get_capacity():

        def it_returns_capacity():
            b = Battery(100)
            assert b.getCapacity() == 100

    def describe_get_charge():

        def it_returns_charge():
            b = Battery(100)
            assert b.getCharge() == 100

    def describe_recharge():

        def it_recharges_drained_battery():
            b = Battery(100)
            b.mCharge = 50
            b.recharge(25)
            assert b.getCharge() == 75

        def it_recharges_drained_battery_to_not_exceed_capacity():
            b = Battery(100)
            b.mCharge = 90
            b.recharge(50)
            assert b.getCharge() == 100

        def it_returns_true_if_recharged():
            b = Battery(100)
            b.mCharge = 25
            result = b.recharge(25)
            assert result

        def it_returns_false_if_amount_invalid():
            b = Battery(100)
            b.mCharge = 50
            result = b.recharge(0)
            assert result == False
            
        def it_returns_false_if_charge_greater_than_capacity():
            b = Battery(100)
            b.mCharge = 110
            result = b.recharge(55)
            assert result == False

        def it_notifys_external_monitor_recharge(mocker):
            mock_monitor = Mock()
            mock_db_notify_recharge = mocker.patch.object(mock_monitor, 'notify_recharge', return_value=None)

            b = Battery(100, mock_monitor)
            b.mCharge = 50
            b.recharge(25)

            mock_db_notify_recharge.assert_called_once_with(75)

        def it_doesnt_notify_external_monitor_recharge(mocker):
            mock_monitor = Mock()
            mock_db_notify_recharge = mocker.patch.object(mock_monitor, 'notify_recharge', return_value=None)

            b = Battery(100, mock_monitor)
            b.mCharge = 110
            b.recharge(25)

            mock_db_notify_recharge.assert_not_called()

    def describe_drain():
        # your test cases here

        def it_drains_full_battery():
            b = Battery(100)
            b.drain(50)
            assert b.getCharge() == 50

        def it_drains_low_battery():
            b = Battery(100)
            b.mCharge = 25
            b.drain(20)
            assert b.getCharge() == 5

        def it_doesnt_drain_lower_than_0():
            b = Battery(100)
            b.drain(110)
            assert b.getCharge() == 0

        def it_returns_false_if_amount_is_invalid():
            b = Battery(100)
            result = b.drain(0)
            assert result == False

        def it_returns_false_if_battery_has_0_charge():
            b = Battery(0)
            result = b.drain(10)
            assert result == False

        def it_returns_true_if_battery_drains():
            b = Battery(100)
            result = b.drain(10)
            assert result
            
        def it_notifys_external_monitor_drain(mocker):
            mock_monitor = Mock()
            mock_db_notify_recharge = mocker.patch.object(mock_monitor, 'notify_drain', return_value=None)

            b = Battery(100, mock_monitor)
            b.drain(25)

            mock_db_notify_recharge.assert_called_once_with(75)

        def it_doesnt_notify_external_monitor_drain(mocker):
            mock_monitor = Mock()
            mock_db_notify_recharge = mocker.patch.object(mock_monitor, 'notify_drain', return_value=None)

            b = Battery(100, mock_monitor)
            b.recharge(0)

            mock_db_notify_recharge.assert_not_called()