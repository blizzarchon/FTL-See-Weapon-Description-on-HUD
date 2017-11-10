
from xml.etree import ElementTree
import re

# def split_str_n_length_parts(string, n):
#
#    """
#    >>> split_str_n_length_parts("helloseventennis", 3)
#    >>> ["hello", "seven", "tenni", "s"]
#    """
#    string_list = []
#    count = 0
#    start = 0
#    for i in range(len(string)):
#        count += 1
#        if count == n:
#            string_list.append(string[start:i + 1])
#            start = i + 1
#            count = 0
#    return string_list


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


def ftl_names(node, fw):
    fw.write("<{} race=\"{}\" sex=\"{}\">"
             "\n".format(node.tag,
                         node.attrib['race'],
                         node.attrib['sex']))
    list_of_names = []
    for name in node:
        if name.tag != 'name':
            raise AttributeError("Bad tag in nameList!\n")
        elif len(name.attrib) > 0:
            # a short attribute exists, just write it
            fw.write("\t<{} short=\"{}\">{}</{}>"
                     "\n".format(name.tag,
                                 name.attrib['short'],
                                 name.text,
                                 name.tag))
        else:
            # no attributes exist
            list_of_names.append(name.text)
    # sort list_of_names in descending order
    # write all the names
    for name in sorted(list_of_names):
        fw.write("\t<name>{}</name>\n".format(name))
    fw.write("</{}>\n\n".format(node.tag))


def ftl_names_v2(node, names, short_names):
    """ Sorts the <name /> tags in node into short_names if the tag contains
        a "short" attribute, or names if the tag is just plain.

    :param node: tree representing a nameList
    :param names: list
    :param short_names: list
    :rtype: None
    """
    for name in node:
        if name.tag != 'name':
            raise AttributeError("Bad tag in nameList!\n")
        elif len(name.attrib) > 0:
            if (name.attrib['short'], name.text) not in short_names:
                short_names.append((name.attrib['short'], name.text))
        else:
            if name.text not in names:
                names.append(name.text)


def write_names(wf, short_male, reg_male, short_female, reg_female):
    """ Writes the names of two nameLists in "alphabetical" order into wf.

    :param wf: a file to write to
    :param short_male: list with the <name="short"> tags for male nameList
    :param reg_male: list with the <name> tags for male nameList
    :param short_female: list with the <name="short"> tags for female nameList
    :param reg_female: list with the <name> tags for female nameList
    :rtype: None
    """
    wf.write("<nameList race=\"human\" sex=\"male\">\n")
    for name_tuple in sorted(short_male):
        wf.write("\t<name short=\"{}\">{}</name>\n"
                 "".format(name_tuple[0], name_tuple[1]))
    for name_string in sorted(reg_male):
        wf.write("\t<name>{}</name>\n"
                 "".format(name_string))
    wf.write("</nameList>\n\n"
             "<nameList race=\"human\" sex=\"female\">\n")
    for name_tuple in sorted(short_female):
        wf.write("\t<name short=\"{}\">{}</name>\n"
                 "".format(name_tuple[0], name_tuple[1]))
    for name_string in sorted(reg_female):
        wf.write("\t<name>{}</name>\n"
                 "".format(name_string))
    wf.write("</nameList>\n")


def xmlize(event_root, writer):
    """ Does XML stuff using event_root as a tree representing a read-only file
        and writer as as a write-only file.

    :param event_root: the head node of a tree containing XML data
    :param writer: a file open for writing
    :rtype: None
    """
    naming = False
    # male_names_list, male_short_names_list = [], []
    # female_names_list, female_short_names_list = [], []
    names_list, short_names_list = [], []
    for child in event_root:
        if ((child.tag == 'weaponBlueprint') and
                ("DRONE" not in child.attrib['name'])):
            tooltips(child, writer)
        if child.tag == 'nameList':
            # ftl_names(child, writer)
            if not naming:
                naming = True
            if child.attrib['sex'] == 'male':
                # names_list was male_names_list
                ftl_names_v2(child, names_list, short_names_list)
            elif child.attrib['sex'] == 'female':
                # names_list was female_names_list
                ftl_names_v2(child, names_list, short_names_list)
            else:
                raise ValueError("nameList's 'sex' attribute must "
                                 "either be male or female!\n")
    if naming:
        # write_names(writer, male_short_names_list, male_names_list,
        #             female_short_names_list, female_names_list)
        write_names(writer, short_names_list, names_list,
                    short_names_list, names_list)


if __name__ == '__main__':

    reading = input("\nEnter name of file in this directory to read from:\n")

    with open(reading, 'r') as reading_file:
        tree = ElementTree.parse(reading_file)
        root = tree.getroot()

        writing = input("Enter name of new file name to write to.\n")
        with open(writing, 'w') as writing_file:
            xmlize(root, writing_file)
