def clone_repos(tools_csv, vendor_repos_dir):
    """
    Clone or update the cross-check repositories
    """

    import os
    from subprocess import call
    from fmpy.cross_check import get_vendor_ids

    vendors = get_vendor_ids(tools_csv)

    for vendor in sorted(vendors.keys()):

        if vendors is None or vendor in vendors:

            clone_url = 'https://github.com/fmi-crosscheck/%s.git' % vendor

            repo_dir = os.path.join(vendor_repos_dir, vendor)

            try:
                print('Pulling %s...' % vendor)
                # revert all changed files
                call(['git', 'reset', '--hard'], cwd=repo_dir)
                # remove untracked files and directories
                call(['git', 'clean', '-fd'], cwd=repo_dir)
                # pull from origin
                call(['git', 'lfs', 'pull'], cwd=repo_dir)
                # TODO: reset --hard, clean -fd
            except Exception as e1:
                # clone the repository if it doesn't exist yet
                print('Cloning %s...' % vendor)
                try:
                    call(['git', 'clone', clone_url], cwd=vendor_repos_dir)
                except Exception as e2:
                    # catch problems like empty repo
                    print(e2)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="Clone or update the cross-check vendor repositories")

    parser.add_argument('tools_csv', help="Path to the tools.csv file from the fmi-standard.org repository")
    parser.add_argument('vendor_repos_dir', help="Directory that contains the vendor repositories")

    args = parser.parse_args()

    clone_repos(tools_csv=args.tools_csv, vendor_repos_dir=args.vendor_repos_dir)