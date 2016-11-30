(NR == FNR){ 				# this will be executed for each line of the first file
    if (NR == 1){			# initialise file dependent constants from header
	cols = NF
	rows = 1
	next;
    }
    # create an array a with all the entries of the first file
    for (i=1; i<=cols; i++){
        a[NR-1,i] = $i
    }
    rows++;
    next;			# skip the rest of the execution and start from the beginning
}

{
    if (FNR == 1){		# for the header line
	if (cols != NF){
	    print "Error: files have different number of columns." > "/dev/stderr"
	    exit 1
	}
	# initialise computation variables
	count = 1
	entries = 1
	norm = 0.0
	next;
    }
    
    if (a[count,1] == $1){
	# print NR, $1, a[count,1]
    	for (i=2; i <= cols; i++) {
	    diff = $i - a[count,i]
	    # print diff, $i, a[count,i]
	    norm += diff*diff
	    entries++
	}
	count++
    }
}

END{
	if (rows != count){
	    print "Warning: files have different number of corresponding rows." > "/dev/stderr"
	}
	print sqrt(norm)/entries
}

