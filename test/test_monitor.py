import pytest
from trials.monitor import getpage, parse_init

# run by:
# py.test -p no:warnings

def prepare_timeanddate_com():
	page = 'https://www.timeanddate.com'
	lookfor = []
	correct = []

	lookfor.append('timeanddate.com##.rd-inner > #clk_hm' )
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com##h2 > a')
	correct.append('<span id="clk_hm">'  )
	lookfor.append('timeanddate.com##.clear') # p clas=clear
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com##.four > .rd-box > .rd-inner > h2')
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com##.four > .rd-box > .rd-inner')
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com###clk_hm')
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com##.rd-inner')
	correct.append( '<span id="clk_hm">' )
	lookfor.append('timeanddate.com##h2')
	correct.append('<span id="clk_hm">'  )

	return [page, lookfor, correct]



def test_parse_init():
	
	tpage, tlookfor, tcorrect = prepare_timeanddate_com()

	sp = getpage(tpage)
	for l,c in zip(tlookfor,tcorrect):
		parsed = parse_init(sp, l)
		assert (str(parsed[0])[:18]) == c,"test failed"
	


def test_met():
	x=5
	y=6
	assert x+1 == y,"test failed" 