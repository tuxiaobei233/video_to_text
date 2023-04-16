from PIL import Image
import imagehash
hash1 = imagehash.phash(Image.open('tests/150-4.jpg'))
print(hash1)
hash2 = imagehash.phash(Image.open('tests/165-4.jpg'))
print(hash2)
print(hash1 - hash2)
