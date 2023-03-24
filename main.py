import argparse
import sys

def parse_srt_file(file_path):
    """Parse an SRT file and return a list of subtitle entries."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
        entries = []
        entry = None
        for line in lines:
            if not entry:
                entry = {'index': int(line), 'times': None, 'text': ''}
            elif not entry['times']:
                start, end = line.split(' --> ')
                entry['times'] = (parse_time(start), parse_time(end))
            elif line.strip() == '':
                entries.append(entry)
                entry = None
            else:
                entry['text'] += line
        if entry:
            entries.append(entry)
    return entries

def parse_time(time_str):
    """Parse a time string in the format '00:00:00,000' and return the number of milliseconds."""
    hours, minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)

def format_time(milliseconds):
    """Format a time in milliseconds as a string in the format '00:00:00,000'."""
    hours = milliseconds // 3600000
    minutes = (milliseconds // 60000) % 60
    seconds = (milliseconds // 1000) % 60
    milliseconds = milliseconds % 1000
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, milliseconds)

def sort_subtitles_by_time(subtitles):
    """Sort a list of subtitle entries by start time."""
    return sorted(subtitles, key=lambda x: x['times'][0])

def save_srt_file(subtitles, file_path):
    """Save a list of subtitle entries to an SRT file."""
    with open(file_path, 'w') as f:
        for i, entry in enumerate(subtitles):
            #f.write('{}\n'.format(entry['index']))
            f.write(str(i)+"\n")
            f.write('{} --> {}\n'.format(format_time(entry['times'][0]), format_time(entry['times'][1])))
            f.write(entry['text'])
            if i < len(subtitles) - 1:
                f.write('\n')


    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    subtitles = parse_srt_file(input_file_path)
    subtitles = sort_subtitles_by_time(subtitles)
    save_srt_file(subtitles, output_file_path)

    print('Sorted subtitles saved to {}'.format(output_file_path))






def main():
    parser = argparse.ArgumentParser(description='Process input and output parameters')
    parser.add_argument('-i', '--input', type=str, help='Input file path')
    parser.add_argument('-o', '--output', type=str, help='Output file path')
    args = parser.parse_args()

    if args.input is None or args.output is None:
        parser.print_help()
        return

    # Use input and output parameters
    print(f'Input file path: {args.input}')
    print(f'Output file path: {args.output}')

    subtitles = parse_srt_file(args.input)
    subtitles = sort_subtitles_by_time(subtitles)
    save_srt_file(subtitles, args.output)

if __name__ == '__main__':
    main()