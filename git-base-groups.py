#!/usr/bin/env python
from __future__ import print_function
import subprocess
'''
	TODO:
		list merge-bases in each group
		filter (tags? branches? remotes? all?)
'''

def main():
	groups = []
	
	refs = subprocess.check_output(['git', 'rev-parse', '--symbolic', '--all'])
	refs = refs.split('\n')
	
	for ref in refs:
		if ref:
			added = False
			for group in groups:
				group_first_ref = group[0]
				try:
					with open('/dev/null', 'w') as null:
						subprocess.check_call(['git', 'merge-base', ref, group_first_ref], stdout=null)
				except subprocess.CalledProcessError:
					pass
				else:
					group.append(ref)
					added = True
					break
			if not added:
				new_group = [ref]
				groups.append(new_group)
	
	for group in groups:
		for ref in group:
			print(ref)
		
		print()
	

if __name__ == '__main__':
	main()
