#!/usr/bin/env python
import os, sys, subprocess, time, yaml

import wasanbon
from wasanbon.core import package, repositories

import unittest

test_dir = os.getcwd()

setting = yaml.load(open('setting.yaml', 'r'))
user_name = setting['user_name']
password = setting['password']

class WSBTest(unittest.TestCase):


    def setup(self):
        os.chdir(test_dir)
        pass

    def test_rtc_create_delete(self):
        pack_name = 'wasanbon_test_package'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'create', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        back_end = 'python'
        comp_name = 'TestComponent'
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'create', comp_name]), 0)
        self.assertTrue(not package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addInPort', comp_name, 'RTC.TimedLong', 'in']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addOutPort', comp_name, 'RTC.TimedLong', 'out']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'delete', comp_name]), 0)
        self.assertTrue(package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])

    def test_repository_create_delete(self):
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'create', '-f', '-u', user_name, '-p', password]), 0)
        self.assertTrue(repositories.is_local_owner_repository(user_name))
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'destroy', '-f', '-u', user_name, '-p', password]), 0)

    def test_package_create_delete(self):
        pack_name = 'wasanbon_test_package'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'create', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])

    def test_cxx_package_clone(self):
        pack_name = 'tutorial01'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        os.chdir('..')
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])


    def test_python_package_clone(self):
        pack_name = 'wsb_test_py_project'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        self.assertEqual(subprocess.call(['./mgr.py', 'system', 'run', '-f']), 0) 
        time.sleep(5)
        sel

        os.chdir('..')
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])


    def test_java_package_clone(self):
        pack_name = 'simvehicle'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        os.chdir('..')
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])

        

if __name__ == '__main__':
    unittest.main()