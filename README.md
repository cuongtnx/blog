# Cuongtn's blog

## Guide

Generate contents using the `publishconf` file.

`pelican -s publishconf.py`

The static version is located in a different folder; thus need to copy contents from current `output` folder into the proper `output` folder; commit & push.

```
cp -r output ~/blog

cd ~/blog/output

git add .

git commit -m "updated blog"

git push origin master
```
