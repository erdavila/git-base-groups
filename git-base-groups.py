#!/usr/bin/env python
from __future__ import print_function
import subprocess
'''
	TODO:
		list merge-bases in each group
		filter (tags? branches? remotes? all?)
'''


class Group(object):
	def __init__(self, base, refs):
		self.base = base
		self.refs = refs


def main():
	groups = []
	
	refs = get_references()
	
	for ref in refs:
		added = False
		for group in groups:
			base = get_base(ref, group.base)
			if base:
				group.refs.append(ref)
				group.base = base
				added = True
				break
		if not added:
			new_group = Group(base=ref, refs=[ref])
			groups.append(new_group)
	
	for group in groups:
		for ref in group.refs:
			print(ref)
		
		print()


def get_references():
	refs = subprocess.check_output(['git', 'rev-parse', '--symbolic', '--all'])
	refs = refs.split('\n')
	for ref in refs:
		if ref:
			yield ref


def get_base(*refs):
	try:
		base_output = subprocess.check_output(['git', 'merge-base'] + list(refs))
	except subprocess.CalledProcessError:
		base = None
	else:
		base = base_output.split('\n')[0]
	return base


if __name__ == '__main__':
	main()
