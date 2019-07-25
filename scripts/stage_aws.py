import nexradaws
import os
import shutil
import tempfile
import sys


def get_month(radar, year, month, odir):
    templocation = tempfile.mkdtemp()
    conn = nexradaws.NexradAwsInterface()
    days = conn.get_avail_days(year, month)
    fls = []
    for day in days:
        print('doing ', day)
        # stage to temp dir
        scans = conn.get_avail_scans(year, month, day, radar)
        localfiles = conn.download(scans, templocation)
        # loop thought files and determine destination
        try:
            for downloaded_file in localfiles.success:
                infile = downloaded_file.filepath
                # os.path.join(downloaded_file.filepath,
                #                      downloaded_file.filename)
                print(downloaded_file.filepath)
                outpath = os.path.join(odir,
                                       radar,
                                       downloaded_file.scan_time.strftime('%Y/%m/%d/'))
                try:
                    os.makedirs(outpath)
                except FileExistsError:
                    pass  # directory exists

                # move to destination
                print(os.path.join(outpath, downloaded_file.filename))
                shutil.move(infile, os.path.join(outpath, downloaded_file.filename))
                fls.append(outpath)
        except TypeError: #catching the case when no files that day
            fls.append("NO data on " + day)

    return fls


if __name__ == '__main__':
    radar = sys.argv[1]
    year = sys.argv[2]
    month = sys.argv[3]
    odir = sys.argv[4]
    _ = get_month(radar, year, month, odir)

