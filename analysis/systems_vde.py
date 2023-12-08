# 15.11.2023
from collections import namedtuple

vde = namedtuple("system", "b3lyp mp2")
systems = {
	21: vde('ammonia-02-1-B3LYP.txt', 'ammonia-02-1-MP2.txt'),
	22: vde('ammonia-02-2-B3LYP.txt', 'ammonia-02-2-MP2.txt'),
	34: vde('ammonia-03-4-B3LYP.txt', 'ammonia-03-4-MP2.txt'),
	41: vde('ammonia-04-1-B3LYP.txt', 'ammonia-04-1-MP2.txt'),
	42: vde('ammonia-04-2-B3LYP.txt', 'ammonia-04-2-MP2.txt'),
	44: vde('ammonia-04-4-B3LYP.txt', 'ammonia-04-4-MP2.txt'),
	51: vde('ammonia-05-1-B3LYP.txt', 'ammonia-05-1-MP2.txt'),
	54: vde('ammonia-05-4-B3LYP.txt', 'ammonia-05-4-MP2.txt'),
	62: vde('ammonia-06-2-B3LYP.txt', 'ammonia-06-2-MP2.txt'),
	71: vde('ammonia-07-1-B3LYP.txt', 'ammonia-07-1-MP2.txt'),
	81: vde('ammonia-08-1-B3LYP.txt', 'ammonia-08-1-MP2.txt'),
	82: vde('ammonia-08-2-B3LYP.txt', 'ammonia-08-2-MP2.txt'),
	83: vde('ammonia-08-3-B3LYP.txt', 'ammonia-08-3-MP2.txt'),
	101: vde('ammonia-10-1-B3LYP.txt', 'ammonia-10-1-MP2.txt'),
	121: vde('ammonia-12-1-B3LYP.txt', 'ammonia-12-1-MP2.txt'),
	122: vde('ammonia-12-2-B3LYP.txt', 'ammonia-12-2-MP2.txt'),
	141: vde('ammonia-14-1-B3LYP.txt', 'ammonia-14-1-MP2.txt'),
	161: vde('ammonia-16-1-B3LYP.txt', 'ammonia-16-1-MP2.txt'),
	201: vde('ammonia-20-1-B3LYP.txt', 'ammonia-20-1-MP2.txt'),
	241: vde('ammonia-24-1-B3LYP.txt', 'ammonia-24-1-MP2.txt'),
	281: vde('ammonia-28-1-B3LYP.txt', 'ammonia-28-1-MP2.txt'),
	321: vde('ammonia-32-1-B3LYP.txt', 'ammonia-32-1-MP2.txt'),
	361: vde('ammonia-36-1-B3LYP.txt', 'ammonia-36-1-MP2.txt'),
	401: vde('ammonia-40-1-B3LYP.txt', 'ammonia-40-1-MP2.txt'),
	481: vde('ammonia-48-1-B3LYP.txt', 'ammonia-48-1-MP2.txt'),
}
