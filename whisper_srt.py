
def convert_time_format(time_str):
    lines = open('1.txt').read().splitlines()

    def convert_time_format(time_str):
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        milliseconds = int(parts[3])
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return f"{total_seconds:0.3f}".replace('.', ',')


    converted_lines = []
    for i, line in enumerate(lines):
        if line.strip():  # Check if the line is not empty
            # Extract the timestamp
            timestamp_parts = line.split("   ")[0].split(' --> ')
            start_time = timestamp_parts[0].replace('.',',').replace('[','')
            end_time = timestamp_parts[1].replace('.',',').replace(']','')

            # Convert timestamp format
            # converted_start_time = convert_time_format(start_time.replace('[',''))
            # converted_end_time = convert_time_format(end_time.replace(']',''))

            # Construct the converted line
            converted_line = f"{i+1}\n{start_time} --> {end_time}\n{line.split("   ")[1]}\n"
            converted_lines.append(converted_line)

    # save to file
    with open('converted.txt', 'w') as f:
        f.write('\n'.join(converted_lines))


def replace_every_third(input_file, output_file):
    with open(input_file, 'r') as f_input:
        lines1 = f_input.readlines()
    with open(output_file, 'r') as f_input:
        lines2 = f_input.readlines()

    output = open("2.srt", 'w')
    for i, line2 in enumerate(lines2):
        if (i + 2) % 4 == 0 and i < len(lines1) * 4:
            output.write(lines1[i//4])
        else:
            output.write(line2)
    output.close()

input_file = '2.txt'  # Change to your input file name
output_file = '1.srt'  # Change to your output file name

replace_every_third(input_file, output_file)
