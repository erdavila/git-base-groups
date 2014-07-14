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
		if is_commit_reference(ref):
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

	groups.sort(key=lambda group:group.base)

	refs_without_common_base = []
	for group in groups:
		if len(group.refs) == 1:
			refs_without_common_base.append(group.refs[0])
		else:
			print("Have common base", group.base + ":")
			for ref in sorted(group.refs):
				print('\t', ref)
			
			print()
	
	if refs_without_common_base:
		print("Without common base:")
		for ref in sorted(refs_without_common_base):
			print('\t', ref)


ref_type = subprocess.Popen(['git', 'cat-file', '--batch-check=%(objecttype)'],
						stdin=subprocess.PIPE,
						stdout=subprocess.PIPE,
						stderr=open('/dev/null', 'w'))
def is_commit_reference(ref):
	print(ref + '^{commit}', file=ref_type.stdin)
	type = ref_type.stdout.readline()
	return type.startswith('commit')


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
