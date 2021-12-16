# At the Catastrophy-Point & The computer as seen at the end of the human age
Complementary code to book [At the Catastrophy-Point](http://carljohanrosen.com#catastrophy). This code was written for [Olle Essvik's](https://www.jimpalt.org/) book *The computer as seen at the end of the human age* to be published early 2022. It generates images to be part of that publication.

## Introduction
There is a point, at which the illusion of a structured geometrical shape dissolves into something else. The artist Manfred Mohr refers to this point using a term taken from mathematics: the catastrophy-point. In 1974, Mohr explored the limits of the cube, which resulted in a series of works. One of these works — a film of two cubes rotating — was my main object of study a few years back. I sought a path from the video surface, through an algorithm, towards the code that created the cubes and their movements. I believe I've found the algorithm (but not the code) and my process is documented in a book called: *At the Catastrophy-Point: The analytical observer's notes on Complementary Cubes*.

The renderings presented in this book represent segments of this algorithm, where multiple cubes are overlaid and viewed from different angles around the vertical axis. I would argue they are beyond the catastrophy-point of the cube, as the renderings have predominantly picked up a curvature foreign to the aesthetics of the cube, but much more aligned to that of rotation.

The algorithm to rotate the cubes can be python-coded like this:

	r = math.pi/180
	x = 83 * math.sin((f - 98) * r) - 7 * math.sin((3 * f + 66) * r) - 90
	y = 30 * math.sin((2 * f - 16) * r)
	z = 83 * math.sin((f - 8) * r) + 7 * math.sin((3 * f + 156) * r) - (f - 518)

where `f` is a frame number. The complete algorithm and the code written to create these images can be found through [carljohanrosen.com#catastrophy](https://carljohanrosen.com#catastrophy).

## Execute
To generate some content similar to what will be published in the book, initate a virtual environment (if you want) and run:

	python thealgorithm.py

Pdf's will now be generated to the `./output` folder.