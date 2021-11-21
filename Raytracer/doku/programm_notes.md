# Notes
*Notes regarding Python Specific libs and features and also regarding own definitions*

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

- **Result must be an 2-Dimensional Array containing an Array of 3-Elements (RGB-Values)**

## Light strength:
- First step: uses strength linearly (needs theory)
$$
\begin{array}{ll}
strength = initial - degredation * distance \\
strength = \sqrt{r^2+g^2+b^2} \\
initial = [255, 255, 255] \\
degradation= [2,2,2]
\end{array}
$$

## Light Interpolation:
- First: 50/50 (needs Theory)
$$
new = \frac{old_1 + old_2}{2}
$$

## Useful Classes:
- First Version: only own classes
### Numpy
- Matrix: represents a Matrix
- Array: represents an array
- 