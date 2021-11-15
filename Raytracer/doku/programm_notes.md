# Notes

## Image Generation
- generate an Array (2-dimensional) which contains the color of every pixel
- Use a lib to create an image (PIL)
    - example:
    ````py
    from PIL import Image
    import numpy as np

    w, h = 512, 512
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()
    ```