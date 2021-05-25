# SqlDiff Development

## Setup
* Use `python 3.9` or later.
* After cloning repo, install packages `pip install -r requirements.txt`
* Set root project directory as working directory in Your IDE.  
* `sqlDiff/sqldiff/main.py` is a main application launch script. Add it to PYTHONPATH.

## Building UI
All resource files and `*.ui` files created by QtDesigner, 
or any similar WYSIWYG tool needs to be placed in `/design` directory.
Use below command to compile `*.ui` and resource files into python objects 
that will be stored in `/sqldiff/ui/designer`:
```
./pyuic_compile_design.sh . design sqldiff/ui/designer
```

## Application Versioning
Use `bumpversion [major|minor|patch|build]` command to update application version. 
Any `bumpversion` call will create `dev0` build, for example: 
'0.0.0' -> 'bumpversion patch' will create version `0.0.1-dev0`

When developing use:
```
`bumpversion [major|minor|patch|build]`
```

If development is finished use:
```
bumpbversion --tag release
```
It will remove `devx` suffix and will create and commit tag in git repo.

## Pull Request
Pull request will trigger application's tests, and test build. 
It must be completed successfully before merging changes into `master` branch.