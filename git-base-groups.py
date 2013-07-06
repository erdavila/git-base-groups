#!/usr/bin/env python
from __future__ import print_function
from collections import namedtuple
import subprocess
'''
	TODO:
		list merge-bases in each group
		filter (tags? branches? remotes? all?)
'''


Group = namedtuple('Group', ['base', 'refs'])


def main():
	groups = []
	
	refs = get_references()
	
	for ref in refs:
		added = False
		for group in groups:
			if have_shared_base(ref, group.base):
				group.refs.append(ref)
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


def have_shared_base(*refs):
	try:
		with open('/dev/null', 'w') as null:
			subprocess.check_call(['git', 'merge-base'] + list(refs), stdout=null)
	except subprocess.CalledProcessError:
		return False
	else:
		return True


if __name__ == '__main__':
	main()
