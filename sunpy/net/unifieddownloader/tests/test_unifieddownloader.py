import datetime
import pytest
import sunpy
import sunpy.net.vso.attrs as attrs 
from sunpy.time.timerange import TimeRange
from sunpy.net.unifieddownloader.downloader_factory import UnifiedDownloader

@pytest.mark.parametrize("time,instrument,client",
[
(attrs.Time('2012/8/8','2012/8/9'),attrs.Instrument('eve'),"EVEClient"),
(attrs.Time('2012/3/5','2012/3/7'),attrs.Instrument('lyra'),"LYRAClient"),
(attrs.Time('2012/1/8','2012/1/9'),attrs.Instrument('norh'),"NoRHClient"),
(attrs.Time('2012/4/22','2012/4/25'),attrs.Instrument('rhessi'),"RHESSIClient"),
#(attrs.Time('2012/1/8','2012/3/9'),attrs.Instrument('noaa-indices'),"NOAAIndicesClient"),
#(attrs.Time('2012/12/8','2012/12/9'),attrs.Instrument('noaa-predict'),"NOAAPredictClient"),
])
def test_query(time,instrument,client):
    
    unifiedresp = UnifiedDownloader.query(time,instrument)
    for block in unifiedresp:
        assert block.client.__class__.__name__ == client


@pytest.mark.online
@pytest.mark.parametrize("time,instrument",
[
(attrs.Time('2013/1/8','2013/1/9'),attrs.Instrument('eve')),
(attrs.Time('2011/5/5','2011/5/6'),attrs.Instrument('lyra')),
(attrs.Time('2012/7/8','2012/7/9'),attrs.Instrument('norh')),
(attrs.Time('2011/1/22','2011/4/25'),attrs.Instrument('rhessi')),
(attrs.Time('2012/1/8','2012/3/9'),attrs.Instrument('noaa-indices')),
(attrs.Time('2012/12/8','2012/12/9'),attrs.Instrument('noaa-predict')),
])
def test_get(time,instrument):
    
    unifiedresp = UnifiedDownloader.query(time,instrument)
    res = UnifiedDownloader.get(unifiedresp)
    download_list = res[0].wait()
    assert len(download_list) == unifiedresp[0].num_records()


@pytest.mark.online
@pytest.mark.parametrize("time1,time2,instrument",
[
(attrs.Time('2012/4/5','2012/4/5'),attrs.Time('2011/8/7','2011/8/7'),attrs.Instrument('norh')),
(attrs.Time('2012/3/3','2012/3/3'),attrs.Time('2013/1/1','2013/1/1'),attrs.Instrument('rhessi')),
(attrs.Time('2012/7/7','2012/7/8'),attrs.Time('2011/7/7','2011/7/8'),attrs.Instrument('lyra')),
(attrs.Time('2012/5/7','2012/5/8'),attrs.Time('2012/5/7','2012/5/8'),attrs.Instrument('eve')),
])
def test_multiple_time(time1,time2,instrument):

    unifiedresp = UnifiedDownloader.query(time1 | time2, instrument)
    num_files_to_download = sum([block.num_records() for block in unifiedresp])
    res = UnifiedDownloader.get(unifiedresp)
    files_downloaded = sum([len(resobj.wait()) for resobj in res])
    assert files_downloaded == num_files_to_download


@pytest.mark.online
@pytest.mark.parametrize("time,instrument1,instrument2",
[
(attrs.Time('2011/12/1','2011/12/4'),attrs.Instrument('eve'),attrs.Instrument('norh')),
(attrs.Time('2011/3/5','2011/3/5'),attrs.Instrument('lyra'),attrs.Instrument('rhessi')),
])
def test_multiple_clients(time, instrument1, instrument2):

    unifiedresp = UnifiedDownloader.query(time, instrument1 | instrument2)
    num_files_to_download = sum([block.num_records() for block in unifiedresp])
    res = UnifiedDownloader.get(unifiedresp)
    files_downloaded = sum([len(resobj.wait()) for resobj in res])
    assert files_downloaded == num_files_to_download


@pytest.mark.online
def test_vso():

    unifiedresp = UnifiedDownloader.query(attrs.Time("2013/3/4 01:00:00","2013/3/4 01:10:00"), attrs.Instrument('aia'),
    attrs.Wave(304,304), attrs.Sample(600))
    num_files_to_download = sum([block.num_records() for block in unifiedresp])
    res = UnifiedDownloader.get(unifiedresp)
    files_downloaded = sum([len(resobj.wait()) for resobj in res])
    assert files_downloaded == num_files_to_download
