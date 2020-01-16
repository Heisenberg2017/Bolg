# coding=utf-8
import re
import os


def write_content(f, content):
    f.write("<code>\n")
    for c in content:
        f.write("%s\n" % c)
    f.write("</code>\n")


def main():
    f = open(r'D:\Users\thinkpad\Bolg\mytools\transltate\source.md',
             'r', encoding='utf-8')
    dst_f = open('dst.md', 'w', encoding='utf-8')

    title = None
    start_write = False
    cmp = False
    content = []
    for line in f.readlines():
        line = line.replace("\n", "")
        line = line.replace("\"", "")
        line = line.replace("* ", "")
        print(line)
        if line.startswith("title: "):
            title = line[7:]
            print("wrtite----", "====== %s ======\n" % title)
            dst_f.write("====== %s ======\n" % title)
            continue
        if line == "<!--more-->":
            start_write = True
            continue

        if not start_write:
            continue

        if line.startswith("####"):
            text = line[5:]
            dst_f.write("==== %s ====\n" % text)
            continue

        if line.startswith("```") and cmp:
            assert content
            write_content(dst_f, content)
            content = []
            cmp = False
            continue
        elif line.startswith("```") and not cmp:
            cmp = True
            continue
        elif cmp:
            content.append(line)
            continue

        img_link = re.match("!\[.*\]\(/images/(.*) ", line)
        if img_link:
            dst_f.write("\n{{%s?600|}}\r\n" % img_link.groups()[0])
            continue

        dst_f.write("%s\n" % line)


if __name__ == '__main__':
    main()
