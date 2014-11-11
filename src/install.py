#!/usr/bin/python

import os

from chroot import Chroot


def main():
	chroot_dir = "/var/local/debian-7-gitlab"
	chroot = Chroot(chroot_dir, "stable", "debian", "amd64")
	if not os.path.exists(chroot_dir):
		chroot.create()
		chroot.add_apt_source("http://ftp.us.debian.org",
			["main", "contrib", "non-free"])

		install_gitlab(chroot)
	else:
		install_gitlab(chroot)


def install_gitlab(chroot):
	pkgs = ["openssh-server", "postfix"]
	chroot.install_pkgs(pkgs)

	if not chroot.package_installed("gitlab"):
		gitlab_deb = "gitlab_7.4.3-omnibus.5.1.0.ci-1_amd64.deb"
		gitlab_deb_url = "https://downloads-packages.s3.amazonaws.com/" \
			"debian-7.6/%s" % gitlab_deb
		chroot.execute("wget", [gitlab_deb_url, "-P", "/tmp"])
		chroot.execute("dpkg", ["-i", "/tmp/%s" % gitlab_deb])
		chroot.execute("gitlab-ctl", ["reconfigure"])

main()
