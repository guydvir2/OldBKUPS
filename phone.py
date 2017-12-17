import csv_handler

calls_output = csv_handler.ReadFile(fname='test_phone.csv')

dates = ['04/2017', '05/2017', '06/2017', '07/2017', '08/2017', '09/2017', '10/2017']
too_long = 20

with open('summry.txt', "w") as report:
    for month in dates:
        call_index = 0
        call_duration = []
        call_duration_secs = 0
        too_long_callls = []
        for call in calls_output.file_content:
            if month in call[1]:  # call[3] == '08/2017':
                # print(call[3], call[2])
                call_duration_secs += int(call[2].split(':')[0]) * 60 + int(call[2].split(':')[1])
                if int(call[2].split(':')[0]) > too_long:
                    too_long_callls.append([call[0], call[1], call[2], call[4]])
                call_index += 1

        hours = call_duration_secs // 3600
        minutes = (call_duration_secs - hours * 3600) // 60
        seconds = call_duration_secs - hours * 3600 - minutes * 60
        report.write("\n~~~~~~~~~~~~~~~ %s totals ~~~~~~~~~~~~~~~\n" % month)
        report.write("Month:%s , Called done:%d, Time: %02d:%02d:%02d\n" % (month, call_index, hours, minutes, seconds))
        report.write("Calls longer than %d minutes:\n" % too_long)
        for longer in too_long_callls:
            report.write(str(longer) + '\n')
