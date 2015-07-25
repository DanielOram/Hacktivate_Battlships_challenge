
//#include <stdlib.h>
#include <stdio.h>

#include "json.h"
#include "json.c"

json_value* read_state(const char *current_state_file_name)
{
	size_t length = 0;
	char *contents = NULL;

	FILE *f = fopen(current_state_file_name, "r");
	if (!f)
	{
		exit(0);
	}
	fseek(f, 0, SEEK_END);
	length = ftell(f);
	fseek(f, 0, SEEK_SET);
	contents = (char*)calloc(length + 1, 1);
	fread(contents, length, 1, f);
	fclose(f);
	return json_parse (contents, length);
}

void process_action(json_value *current_state)
{
	if (current_state->type != json_object)
	{
		return;
	}
	for(int i=0; i<current_state->u.object.length; i++)
	{
		json_object_entry *entry = current_state->u.object.values+i;
		//TODO

	}
}

int main(int argc, char **argv)
{

	/* Get our input and output filenames */
	const char *current_state_file_name = argv[argc - 2];
	const char *current_move_file_name = argv[argc - 1];


	/* Read the state from disk */
	json_value *current_state = read_state(current_state_file_name);

	if (current_state)
	{
		process_action(current_state);
	}

	/* Freedom! */
	json_value_free (current_state);

	/* All done! */
	return 0;
}