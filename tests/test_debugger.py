import sys

import mock

from hurricane.server.debugging import setup_debugpy, setup_pycharm
from hurricane.testing import HurricanServerTest


class HurricanDebuggerServerTest(HurricanServerTest):

    alive_route = "/alive"

    @HurricanServerTest.cycle_server(args=["--debugger"])
    def test_debugger(self):
        res = self.probe_client.get(self.alive_route)
        out, err = self.driver.get_output(read_all=True)
        self.assertEqual(res.status, 200)
        self.assertIn("Listening for debug clients at port 5678", out)

    def test_debugger_import_debugpy(self):
        sys.modules["debugpy"] = None
        options = {"debugger": True}
        setup_debugpy(options)

    def test_pycharm_import_pydevd_pycharm(self):
        sys.modules["pydevd_pycharm"] = None
        options = {"pycharm_host": "test"}
        setup_pycharm(options)

    def test_debugger_success(self):
        options = {"debugger": True, "debugger_port": 8071}
        with mock.patch("debugpy.listen") as dbgpy:
            dbgpy.side_effect = None
            setup_debugpy(options)

    def test_pycharm_success(self):
        options = {"pycharm_host": "test", "pycharm_port": 8071}
        with mock.patch("pydevd_pycharm.settrace") as pdvd:
            pdvd.side_effect = None
            setup_pycharm(options)
