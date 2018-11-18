# -*- coding: utf-8 -*-
"""
A module that helps with running and maintaining bossfight.server processes.
"""

import threading
import subprocess
import ifaddr
from bossfight.client import config

_RUNNING_PROCESSES = {}
_UPDATE_THREAD = threading.Thread()


def get_running_processes():
    """
    Returns an iterable list of *pid*s of running server processes.
    """
    return list(_RUNNING_PROCESSES.keys()).copy()


def _update_processes():
    while _RUNNING_PROCESSES:
        for pid in get_running_processes():
            try:
                if _RUNNING_PROCESSES[pid]["process"].wait(timeout=0.3) is not None:
                    del _RUNNING_PROCESSES[pid]
            except (subprocess.TimeoutExpired, KeyError):
                pass


def get_available_ip_addresses():
    """
    Returns a list of all available IP addresses the server can be bound to.
    Keep in mind that `127.0.0.1` is only suitable for local servers.
    """
    addresses = []
    for adapter in ifaddr.get_adapters():
        for ip_addr in adapter.ips:
            if ip_addr.is_IPv4 and ip_addr.ip[:3] in {"10.", "172", "192", "127"}:
                # only local IPv4 addresses
                addresses.append(ip_addr.ip)
    return addresses


def run_server(ip_address="localhost", port=0):
    """
    Starts a server bound to the specified address and return the process ID.
    """
    global _UPDATE_THREAD
    cmd = config.get.local_server_exec.copy()
    cmd.extend([ip_address, str(port)])
    server_process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE
    )
    _RUNNING_PROCESSES[server_process.pid] = {
        "process": server_process,
        "ip_address": str(server_process.stdout.readline(), "utf-8").strip(),
        "port": int(server_process.stdout.readline()),
    }
    if not _UPDATE_THREAD.is_alive():
        _UPDATE_THREAD = threading.Thread(target=_update_processes)
        _UPDATE_THREAD.start()
    return server_process.pid


def get_ip_address(pid):
    """
    Returns the the IP address of the server running under the
    process ID *pid*.
    """
    return _RUNNING_PROCESSES[pid]["ip_address"]


def get_port(pid):
    """
    Returns the the port of the server running under ther process ID *pid*.
    """
    return _RUNNING_PROCESSES[pid]["port"]


def get_server_address(pid):
    """
    Returns the server address as a tuple containing IP address and port.
    """
    return (get_ip_address(pid), get_port(pid))


def shutdown(pid):
    """
    Terminates the server process with process ID *pid*.
    """
    try:
        _RUNNING_PROCESSES[pid]["process"].communicate(
            input="shutdown\n".encode("utf-8"), timeout=1.0
        )
        del _RUNNING_PROCESSES[pid]
    except subprocess.TimeoutExpired:
        _RUNNING_PROCESSES[pid]["process"].terminate()
        del _RUNNING_PROCESSES[pid]
    except KeyError:
        return


def clean_up():
    """
    Terminates all running server processes.
    """
    for pid in get_running_processes():
        shutdown(pid)
