# Resize Images
Bulk resizes and/or compress images.

# Requirement
- Poetry >= 1.1.13 [https://python-poetry.org/](https://python-poetry.org/)
- Python >= 3.8
- 
## Usage
### Set up
* Install dependencies
```bash
    poetry install
```
#### Optional:
* There is a [in](in/) default folder to put images in to be resized/compress but an alternative folder
and be specified by setting the `IMAGES_IN_FILE_PATH` environment veriable:
```bash
export IMAGES_IN_FILE_PATH=<folder-path>
```

### To run
```bash
    poetry run resize-image
```

The resized/compressed images will be found in the [out](out/) folder.