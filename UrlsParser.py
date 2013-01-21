#!/usr/bin/env python
# coding: utf-8
"""
*** Warning: This code works but is extremely hacky, patches welcome ***
"""
import re

class LineData:
	parsStr = ""
	expectation = ""
	found = "NO"
	passTest = False

	def __init__(self, parsStr, expectation):
		self.parsStr = parsStr
		self.expectation = expectation

	def setFound(self, found):
		self.found = found
		if found == self.expectation:
			self.passTest = True


class UrlParser:
	URL_REGEX = [
		# 0 got from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
		r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))
		    +(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
		# 1 got from http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python
		r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|
		(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""",
		# 2 got from http://stackoverflow.com/questions/161738/what-is-the-best-regular-expression-to-check-if-a-string-is-a-valid-url
		r"^(ftp|http|https)://([_a-z\d\-]+(.[_a-z\d\-]+)+)(([_a-z\d\-\./]+[_a-z\d\-\/])+)*/*",\
		# 3 byt this spec http://www.apps.ietf.org/rfc/rfc3986.html
		r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(\#(.*))?",
        # 4 http://stackoverflow.com/questions/82398/how-to-match-uris-in-text#83378
		r"""\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*""",
        # 5
        r"""(http|https|ftp|mailto|tel):\S+[/a-zA-Z0-9]""",
        # 6
        r"""^((ht|f)tp(s?)\:\/\/|~/|/)?([\w]+:\w+@)?([a-zA-Z]{1}([\w-]+.)+([\w]{2,5}))
            (:[\d]{1,5})?((/?\w+/)+|/?)(\w+.[\w]{3,4})?((\?\w+=\w+)?(&\w+=\w+)*)?""",
        #7
        r"""(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]"""
	]

	TEST_DATA_FILE = "testData.txt"

	def __init__(self):
		self.startTest()

	def startTest(self):
		file = open(self.TEST_DATA_FILE, "r")
		self.data = [line.split("|") for line in file.read().splitlines()\
				 if line.strip() != ""]
		file.close()

		self.result = []

		for regex in self.URL_REGEX:
			lines = [LineData(element[1],element[2]) for element in self.data if len(element) == 3]
			regObj = re.compile(regex, re.X)
			self.parseStringsWithReg(lines, regObj)
			self.result.append(lines)


		self.printResult()


	def parseStringsWithReg(self, lines, regObj):
		for line in lines:
			expect = regObj.search(line.parsStr)
			if expect and expect.group(0):
				line.setFound(expect.group(0))
			else:
				if line.expectation == "":
					line.setFound("")



	def printResult(self):
		for idx, regex in enumerate(self.URL_REGEX):
			print "%2d %s" % (idx + 1, regex)
		print "\n"

		for idx, sample in enumerate(self.data):
			print repr(idx + 1).rjust(2),
			print repr(sample[0]).ljust(15),
			for i,lines in enumerate(self.result):
				if i+1 < len(self.result):
					print repr(lines[idx].passTest).center(8),
				else:
					print repr(lines[idx].passTest).center(8)



if __name__ == '__main__':
    urlsParser = UrlParser()