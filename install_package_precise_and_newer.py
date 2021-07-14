#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#

import pygtk
pygtk.require("2.0")
import gtk
import apt
import apt.progress.gtk2
import apt_pkg
from apt.cache import Cache
from apt.cache import LockFailedException

class InstallPackageDialog(gtk.Dialog):
	def __init__(self,packages = None):
		title = 'Y PPA Manager - Install package(s)'
		gtk.Dialog.__init__(self,title,None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CLOSE,gtk.RESPONSE_ACCEPT))
		self.set_wmclass = 'Y-PPA-Manager'
		self.set_icon_name('y-ppa-manager')
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.set_size_request(400, 200)
		self.set_resizable(False)
		self.connect('destroy', self.close_application)
		#
		vbox0 = gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		frame2 = gtk.Frame()
		vbox0.add(frame2)
		table2 = gtk.Table(rows = 2, columns = 2, homogeneous = False)
		table2.set_border_width(5)
		table2.set_col_spacings(5)
		table2.set_row_spacings(5)
		frame2.add(table2)
		#
		label11 = gtk.Label('Package(s) to install:')
		label11.set_alignment(0,.5)
		table2.attach(label11,0,1,0,1, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		#
		self.entry12 = gtk.Entry()
		if packages:
			self.entry12.set_text(packages)
		self.entry12.connect('key-press-event',self.on_key_press)
		table2.attach(self.entry12,1,2,0,1, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		#
		button22 = gtk.Button('Install')
		button22.connect('clicked',self.install_package)
		table2.attach(button22,0,2,1,2, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		self.progress = apt.progress.gtk2.GtkAptProgress()
		self.progress._expander.connect('activate',self.on_progress_activate)
		table2.attach(self.progress,0,2,2,3, xoptions = gtk.EXPAND|gtk.FILL, yoptions = gtk.SHRINK)
		#
		self.show_all()
		if packages:
			self.install_package(None)

	def on_key_press(self,widget,event):
		if self.entry12.get_text() != '' and (event.keyval == 65293 or event.keyval ==65421):
			self.install_package(None)
			
	def on_progress_activate(self,widget):
		if self.progress._expander.get_expanded():
			self.set_size_request(400, 200)
		else:
			self.set_size_request(800, 650)
		
	def close_application(self,widget):
		self.hide()
		self.destroy()
		
	def install_package(self,widget):
		cache = apt.cache.Cache(self.progress.open)
		packages = self.entry12.get_text().strip().split()
		for p in packages:
			print p
		inpackages = []
		nopackages = []
		noupgradables = []

		for package in packages:
			try:
				print "%s is installed %s and is upgradable %s"%(package,cache[package].is_installed,cache[package].is_upgradable)
				if cache[package].is_installed and not cache[package].is_upgradable:
					noupgradables.append(package)
				else:
					inpackages.append(package)
			except KeyError,e:
				print e
				nopackages.append(package)
		if len(noupgradables)>0 or len(nopackages)>0:
			message = "<b>Some errors found:</b>\n"
			if len(noupgradables)>0:
				if len(noupgradables)>1:
					tpackages = ', '.join(noupgradables)
					message += "\nThe packages: '%s'\n <b>can't be upgraded</b> or the latest version is already installed"%tpackages
				else:
					message += "\nThe package: %s <b>can't be upgraded</b> or the latest version is already installed"%noupgradables[0]
			if len(nopackages)>0:
				if len(nopackages)>1:
					tpackages = ', '.join(nopackages)
					message += "\nThere are <b>no packages</b> called:\n '%s'"%tpackages
				else:
					message += '\nThere is <b>no package</b> called "%s"'%nopackages[0]
				dbuttons=gtk.BUTTONS_OK
			if len(inpackages)>0:
				if len(inpackages)>1:
					tpackages = ', '.join(inpackages)
					message += "\n<b>Only</b> these packages: '%s'\n will be installed"%tpackages

				else:
					message += "\n<b>Only</b>: %s will be installed"%inpackages[0]
				message +="\n\n<b>Continue?</b>"
				ans_exit = False
				dbuttons=gtk.BUTTONS_YES_NO
			else:
				message += "\n\nThere is <b>no package</b> to install"
				message += "\nInstallation will <b>not continue</b>"
				ans_exit = True
				dbuttons=gtk.BUTTONS_OK
			md = gtk.MessageDialog(parent=self,
			flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			type=gtk.MESSAGE_ERROR,
			buttons=dbuttons,
			message_format=None)
			md.set_markup(message)
			ans = md.run()
			print ans
			if ans == -9 or ans_exit:
				md.destroy()
				exit(0)
			md.destroy()
		print inpackages
		if len(inpackages)>0:
			for inpackage in inpackages:
				if cache[inpackage].is_upgradable:
					cache[inpackage].mark_upgrade()
				else:
					cache[inpackage].mark_install(auto_fix=True, auto_inst=True, from_user=True)
			try:
				self.set_size_request(800, 650)
				self.progress.show_terminal(expanded=True)
				cache.commit(self.progress.acquire, self.progress.install)					
			except LockFailedException,e:
				print e
				md = gtk.MessageDialog(parent=self,
				flags= gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
				type=gtk.MESSAGE_ERROR,
				buttons= gtk.BUTTONS_OK,
				message_format="You didn't run this program as root or another package\nmanager such as Synaptic or apt-get is running")
				md.run()
				md.destroy()
				self.progress.show_terminal(expanded=False)
				self.set_size_request(400, 200)
		else:
			md = gtk.MessageDialog(parent=self,
			flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			type=gtk.MESSAGE_ERROR,
			buttons=gtk.BUTTONS_OK,
			message_format="You didn't enter any package to install!")
			md.run()
			md.destroy()
		self.progress.show_terminal(expanded=False)
		self.set_size_request(400, 200)

if __name__ == '__main__':
	import sys
	if len(sys.argv)>2:
		packages = (' '.join(sys.argv[1:])).strip()
	elif len(sys.argv) >= 2:
		packages = sys.argv[1]
	else:
		packages = None
	ipd = InstallPackageDialog(packages)
	ipd.run()
