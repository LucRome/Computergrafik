# Raytracing:
- Useful Website: [scratchapixel.com](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-ray-tracing/raytracing-algorithm-in-a-nutshell)

## In Nature:
- Light rays are emitted from a source
- When hitting an Object they bounce of in every possible direction (because the Object isn't plain under the microscope)
- There are also other effects like absorption, See-throug elements and Mirror-like Elements
- Simulating this process would mean casting many rays until you find one that hits the viewers eye
    - Very big Overhead

## In Computergraphics:
- Rays are cast from the eye into the scene (backward-ray-tracing)
- If they are reflected and hit a light source, they are light-rays and the surface point is iluminated
- If not they are shadow rays 
- With this process we are able to also simulate other effects (reflection, ...)

### simple Algorithm (Ch. 3):
- ![](https://www.scratchapixel.com/images/upload/introduction-to-ray-tracing/lightingnoshadow.gif)
- For every pixel in the image one ray is shot, the direction of that ray is determined by tracing a line from the eye to the center of the pixel (-> Primary Ray)
- then every object in the image is checked to see if it that ray hits something
- if it hits something:
    - select object with closest intersection point
    - then cast a ray from the intersection point towards the light (Shadow Ray)
        - reaches light -> illuminated
        - hits object -> shadow
- **simple but very time consuming algorithm**

### Reflection and Refraction (Ch.4):
- useful for glass and mirror surfaces
- depend on the direction of the ray and on the normal-vector at the intersect point
