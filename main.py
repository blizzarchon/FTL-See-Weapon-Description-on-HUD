
from xml.etree import ElementTree
import re

def tooltips(node, file):
    """ Puts the description of a weapon into the flavorType tooltip thing.

    :param node: tree representing a weaponBlueprint
    :param file: file open for writing
    :rtype: int|None
    """
    description = ''
    for element in node:
        if (element.tag == 'desc') and (element.text != ''):
            description = element.text
            break
    else:
        # to disregard empty or nonexistent desc tags
        return 5
    # list of indices of periods in the description
    # e.g. "Hello. My Name is. Bob.", indices are 5, 17, 22
    indices = [m.start() for m in re.finditer("\.", description)]
    file.write("<mod:findName type=\"weaponBlueprint\" name=\"{}\">\n"
               "".format(node.attrib['name']))

    file.write("\t<mod-overwrite:flavorType>")

    temp_desc, prior_index = description, 0
    # prior_index is used to offset the temp_desc substring so that indices[]
    # can still be referred to. (length of "Hello. " is prior_index, 7)
    #   description = "Hello. My Name is. Bob." indices are [5, 17, 22]
    #   temp_desc = "My name is. Bob." sentence indices are    [10, 15]
    for index in indices:
        if index != indices[-1]:
            # the current sentence, index is location of the end period
            temp_desc = temp_desc[:index - prior_index + 1]
            file.write(temp_desc + " a\n")
            new_start = index + 2
            # the new description is everything after the first sentence
            temp_desc = description[new_start:]
            prior_index = new_start
    # even if no periods are in description, it'll still be added to flavorType
    file.write("{}</mod-overwrite:flavorType>\n".format(temp_desc))

    file.write("</mod:findName>\n\n")


def xmlize(event_root, writer):
    """ Does XML stuff using event_root as a tree representing a read-only file
        and writer as as a write-only file.

    :param event_root: the head node of a tree containing XML data
    :param writer: a file open for writing
    :rtype: None
    """
    for child in event_root:
        if ((child.tag == 'weaponBlueprint') and
                ("DRONE" not in child.attrib['name'])):
            tooltips(child, writer)


if __name__ == '__main__':

    reading = input("\nEnter name of file in this directory to read from:\n")

    with open(reading, 'r') as reading_file:
        tree = ElementTree.parse(reading_file)
        root = tree.getroot()

        writing = input("Enter name of new file name to write to.\n")
        with open(writing, 'w') as writing_file:
            xmlize(root, writing_file)
