#!/usr/bin/perl -w
# use strict;
use warnings;

######################################################################
# generates tablemacro with the parameters of the table for the latex
# compilation

# parse command line parameters
($N=(@files=@ARGV))<=3 or die "maximum three args not $N please\n";

print "\\newcommand{\\tablemacro}{\n"; # starts the macro
# the body
print "\\includegraphics{$files[0]} &\n";
print "\\includegraphics{$files[1]} &\n";
if ($N>2){
    print "\\includegraphics{$files[2]}";
}
print "\\\\\n(a) & (b) &";

if ($N>2){
    print "(c)\n";
}
print "}\n";			# end the macro
