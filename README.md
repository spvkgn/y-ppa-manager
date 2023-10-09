# Y PPA Manager
## Y PPA Manager features:
- Add PPA
- Remove PPA
- Purge PPA
- Search for packages in Launchpad PPAs: a regular search which is faster, but doesn't display exact package matches and comes with less details and a deep search which displays exact package matches. In the search, you can also see if a PPA is already added on your system or not and if a package is already installed (and the installed version). You can perform the following actions on a PPA listed in the search results: add it, list packages in the PPA, open PPA in browser, download packages, install a package using the built-in installer (if the PPA is not already added, it will be added)
- Update single PPAs - without running a full "apt-get update", which should be a lot faster (and especially useful for computers with slow Internet connections)
- List packages in PPAs enabled on your computer
- Edit PPA source file
- Remove duplicate PPAs
- Import all missing GPG keys
- Fix GPG BADSIG errors
- Backup an restore PPAs (automatically imports missing GPG keys)
- Re-enable working PPAs after Ubuntu upgrade: when you upgrade to a newer Ubuntu release, the PPAs are disabled so using this feature, the PPAs that work with the new Ubuntu version you're using are re-enabled, leaving the others disabled
- Update release name in working PPAs: somewhat similar to the feature above, this one is useful if you've backup up the PPAs in say Ubuntu Precise and restored them in Ubuntu Quantal (just an example) - in this case, using this feature you can replace "precise" in each PPA source with "quantal", but only for the PPAs that have packages for Quantal.
- Desktop integration: notifications, Unity quicklists, indicator and HUD support

### Settings:
- PPA Purge behavior: auto - don't require any user input; manual - opens a terminal window asking the user how to solve the issue (this is the default and highly recommended behavior).
- Ubuntu version: this only affects the search. So if you want the Y PPA Manager search to display packages for some other Ubuntu version, simply change the Ubuntu version here. Supported versions: karmic, lucid, maverick or natty (use the Ubuntu version names for Linux Mint too!).
