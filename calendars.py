from datetime import datetime, timedelta
import json
##
import helpers

ignorewords_file = open('words_to_ignore.txt')
monthnames_file = open ('month_names.json')

WORDS_TO_IGNORE = ignorewords_file.readlines()
MONTH_NAME_DICT = json.load(monthnames_file)

ignorewords_file.close()
monthnames_file.close()


class Calendar:
    def __init__(self, raw_text:str, year:str):
        self.year = int(year)
        self.events = {}
        self.processed_text = ''
        self.flagged_lines = []
        line_index = 1
        for line in raw_text.split('\n'):
            stripped_line = helpers.remove_bracketed_words(line).lstrip() # strip leading spaces to prevent buildup
            if stripped_line.count(' ') != len(stripped_line): # if not an empty line
                self.processed_text += f'<{line_index}> ' + stripped_line + '\n'
                event_details = {'month': None, 'day': None, 'description': None}
                running_description = ''
                for word in stripped_line.split(' '):
                    if not (event_details['month'] != None != event_details['day']):
                        if not word.lower() in WORDS_TO_IGNORE:
                            if word.isnumeric() and int(word) <= 31:
                                event_details['day'] = int(word)
                            else:
                                event_details['month'] = self.month_lookup(word)
                    else:
                        running_description += word + ' '

                event_details['description'] = running_description

                if event_details['month'] != None != event_details['day']:
                    event_date = datetime(self.year, event_details['month'], event_details['day'])
                    event_obj = Event(event_date, event_details['description'])
                    self.add_event(event_obj)
                else:
                    self.flagged_lines.append(line_index)
                
                line_index += 1
        self.processed_text = self.processed_text[:-1] # remove the terminal newline


    def month_lookup(self, word):
        query = word[:3].lower()
        return MONTH_NAME_DICT.get(query, None)
    

    def add_event(self, event):
        event_date = event.date
        if event_date in self.events:
            self.events[event_date] = self.events[event_date] + [event]
        else:
            self.events[event_date] = [event]

    
    def month_table(self, month_number:int):
        working_table = '''
        <table>
            <tr>
                <th>Sunday</th>
                <th>Monday</th>
                <th>Tuesday</th>
                <th>Wednesday</th>
                <th>Thursday</th>
                <th>Friday</th>
                <th>Saturday</th>
            </tr>
            <tr>
        '''
        first_day = datetime(self.year, month=month_number, day=1)
        current_day = first_day
        weekday = (first_day.weekday() + 1) % 7# reset such that index 0 is Sun instead of Mon
        working_table += '<td></td>' * weekday
        while first_day.month == current_day.month:
            daily_events = ('<ul><li>' + '</li><li>'.join([event.description for event in self.events[current_day]]) + '</li></ul>') if current_day in self.events else ''
            working_table += f'<td>{current_day.day}<br>{daily_events}</td>'
            current_day += timedelta(days=1)
            weekday = helpers.add_weekday(weekday)
            if weekday == 0:
                working_table += '</tr><tr>'
        
        working_table += '</tr></table>'

        return working_table


    def year_tables(self):
        year_data = {}
        for month in range(1, 13):
            month_name = datetime(self.year, month, 1).strftime('%B')
            month_table = self.month_table(month)
            year_data[month] = {'name':month_name, 'caltable':month_table}
        return year_data
                    

class Event:
    def __init__(self, date, description):
        self.date = date
        self.description = description


if __name__ == '__main__':
    file = open('sample_calendar.txt')
    rawtext = file.read()
    file.close()
    Calendar(rawtext, 2021)