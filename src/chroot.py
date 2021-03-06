#!/usr/bin/python

import os
import subprocess
import shutil
from exceptions import Exception


#
# This class only works on Debian like systems.
#
class Chroot:
	def __init__(self, path, suite, distro, arch, apt_repo = ""):
		if len(path) < 1:
			raise Exception("chroot dir was not specified")

		self.path = path
		self.suite = suite
		self.distro = distro
		self.arch = arch
		self.apt_repo = apt_repo


	#
	# Creates new chroot.
	#
	def create(self):
		retval = subprocess.call(["debootstrap", "--foreign", \
			"--arch=" + self.arch, self.suite, self.path, \
			self.apt_repo])
		if retval != 0:
			raise Exception("Failed to create chroot.")

		self.execute("/debootstrap/debootstrap", \
			["--second-stage"])

		shutil.copyfile("/etc/resolv.conf", \
			self.path + "/etc/resolv.conf")


	#
	# Executes the specified command inside chroot. Returns whatever the
	# executed command returns.
	#
	def execute(self, command, args):
		return subprocess.call(["chroot", self.path, command] + args)


	def add_apt_source(self, url, components):
		apt_sources_file = self.path + "/etc/apt/sources.list"
		with open(apt_sources_file, "a") as f:
			f.write("deb " + url + "/" + self.distro + " " \
				+ self.suite + " " + str.join(" ", components) \
				+ "\n")
			f.close()

		self.execute("apt-get", ["update"])


	#
	# Installs the specified list of packages into chroot.
	#
	def install_pkgs(self, pkgs):
		self.execute("apt-get", ["-y", "install"] + pkgs)


	#
	# Returns true inf the specified package is installed in the chrooted
	# system.
	#
	def package_installed(self, pkg_name):
		return self.execute("dpkg-query", ["-s", pkg_name]) == 0
