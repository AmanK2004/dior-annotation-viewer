import os
import cv2
import xml.etree.ElementTree as ET

image_dir = "JPEGImages-test"
annotation_dir = "Annotations"
test_list = "test.txt"

with open(test_list, "r") as f:
    image_ids = [line.strip() for line in f.readlines()]

for img_id in image_ids[:3]:
    image_path = os.path.join(image_dir, f"{img_id}.jpg")
    annotation_path = os.path.join(annotation_dir, f"{img_id}.xml")

    if not os.path.exists(image_path) or not os.path.exists(annotation_path):
        print(f"Skipping {img_id}: file missing")
        continue

    image = cv2.imread(image_path)
    tree = ET.parse(annotation_path)
    root = tree.getroot()

    for obj in root.findall("object"):
        label = obj.find("name").text
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(image, label, (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

    cv2.imshow(f"{img_id}.jpg", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
