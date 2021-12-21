# At the Catastrophy-Point
Code following up on the book [At the Catastrophy-Point](http://carljohanrosen.com#catastrophy). 

## The computer as seen at the end of the human age
Some of this code was written for [Olle Essvik's](https://www.jimpalt.org/) book *The computer as seen at the end of the human age*, to be published early 2022. It generates images to be part of that publication.

There is a point, at which the illusion of a structured geometrical shape dissolves into something else. The artist Manfred Mohr refers to this point using a term taken from mathematics: the catastrophy-point. In 1974, Mohr explored the limits of the cube, which resulted in a series of works. One of these works — a film of two cubes rotating — was my main object of study for quite some time. I sought a path from the video surface, through an algorithm, towards the code that created the cubes and their movements. I believe I've found the algorithm (but not the code) and my process is documented in a book called: *At the Catastrophy-Point: The analytical observer's notes on Complementary Cubes*.

The renderings presented in this book represent this algorithm in segments, where multiple cubes are overlaid and viewed from fixed angles around the vertical axis. I would argue they are beyond the catastrophy-point of the cube, as the renderings have predominantly picked up a curvature foreign to the aesthetics of the cube, but much more aligned to that of rotation. It is, however, just as true to and dependent on the algorithm that Mohr designed.

This simple algorithm shapes the world alongside other algorithms. The point where algorithms allowed themselves to be deconstructed, reverse-engineered and reconfigured based solely on their output might already be passed. If there was ever such a point.

The complete algorithm and the code written to create these images can be found in this repo.

### Execute
To generate some content similar to what will be published in *The computer as seen at the end of the human age*, initate a virtual environment (if it suits you) and run:

	python endofhuman.py

Pdf's will now be generated to the `./output` folder.

## The algorithm
This repo contains the algorithm discovered through the research process documented in *At the Catastrophy-Point: The analytical observer's notes on Complementary Cubes* (2016)

The algorithm to rotate the cubes can be python-coded like this:

	r = math.pi/180
	x = 83 * math.sin((f - 98) * r) - 7 * math.sin((3 * f + 66) * r) - 90
	y = 30 * math.sin((2 * f - 16) * r)
	z = 83 * math.sin((f - 8) * r) + 7 * math.sin((3 * f + 156) * r) - (f - 518)

where `f` is a frame number. For the complete algorithm, have a look at [cubes.py](https://github.com/cjrosen/at-the-catastrophy-point/blob/main/src/mohr/cubes.py)
