# motivated by http://stackoverflow.com/questions/1729824/transpose-a-file-in-bash
# the first loop will create an array a with all the entries
{ 				# this will be executed at each line
    for (i=1; i<=NF; i++)  {
        a[NR,i] = $i
    }
}
# after the program finishes the array is transposed and printed
END {    			# this is executed only after the END line
    for(j=1; j<=NF; j++) {
        str=a[1,j]		# initialise 'str' to the first entry in the column 'j'
        for(i=2; i<=NR; i++){
            str=str"\t"a[i,j];	# append each following entry from the column to the 'str'
        }
        print str		# print the whole columnn 'j' as a row
    }
}
