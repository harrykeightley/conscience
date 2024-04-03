"""
Ensure that mocking correctly captures subsequent calls to methods.
"""

from director.mocking import MixinBase
import unittest
import traceback


class MockMe:
    def __init__(self, on_call):
        self.on_call = on_call

    def no_args(self):
        self.on_call()

    def single_arg(self, p0):
        self.on_call(p0)

    def many_positional(self, p0, p1, p2, p3):
        self.on_call(p0, p1, p2, p3)

    def single_kw(self, kw0=None):
        self.on_call(kw0)

    def both_args(self, p0, p1, kw0=None, kw1=None):
        self.on_call(p0, p1, kw0=kw0, kw1=kw1)


class DropCalls(MixinBase):
    pass


class TestCoreMock(unittest.TestCase):

    def test_mock(self):
        """test the basic ability to mock where calls are simply replaced"""
        mock1 = DropCalls(MockMe, "no_args")
        mock2 = DropCalls(MockMe, "single_arg")
        mock3 = DropCalls(MockMe, "many_positional")
        mock4 = DropCalls(MockMe, "single_kw")
        mock5 = DropCalls(MockMe, "both_args")

        def fail_if_called(*args, **kwargs):
            traceback.print_stack(f=None, limit=None, file=None)
            self.fail(
                f"a call to MockMe was made bypassing mocking, args: {args} kwargs: {kwargs}"
            )

        mock_me = MockMe(fail_if_called)
        mock_me.no_args()
        mock_me.single_arg("p0")
        mock_me.many_positional("p0", "p1", "p2", "p3")
        mock_me.single_kw(kw0=None)
        mock_me.both_args("p0", "p1", kw0=None, kw1=None)

        # clean up environment - TODO: recreate MockMe to not rely on restore
        mock1.restore()
        mock2.restore()
        mock3.restore()
        mock4.restore()
        mock5.restore()

    def test_restore(self):
        mock = DropCalls(MockMe, "no_args")
        mock.restore()
        mock = DropCalls(MockMe, "single_arg")
        mock.restore()
        mock = DropCalls(MockMe, "many_positional")
        mock.restore()
        mock = DropCalls(MockMe, "single_kw")
        mock.restore()
        mock = DropCalls(MockMe, "both_args")
        mock.restore()

        calls = []

        def record_call(*args, **kwargs):
            calls.append((args, kwargs))

        mock_me = MockMe(record_call)
        mock_me.no_args()
        mock_me.single_arg("p0")
        mock_me.many_positional("p0", "p1", "p2", "p3")
        mock_me.single_kw(kw0=None)
        mock_me.both_args("p0", "p1", kw0=None, kw1=None)

        self.assertEqual(calls[0], (tuple(), {}))
        self.assertEqual(calls[1], (("p0",), {}))
        self.assertEqual(calls[2], (("p0", "p1", "p2", "p3"), {}))
        self.assertEqual(calls[3], ((None,), {}))  # weird behaviour
        self.assertEqual(calls[4], (("p0", "p1"), {"kw0": None, "kw1": None}))


if __name__ == "__main__":
    unittest.main()
