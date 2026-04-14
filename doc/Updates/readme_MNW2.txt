Changes to the MNW2 Package for MODFLOW-2005 version 1.12   (May 2015-Nov. 2016)

A bug was fixed that affected the calculation of intraborehole flow (initiated 
when PUMPLOC is not = 0) for output purposes only and only for certain conditions. 
These values are written to the MNWOBS file if QBHflag>0. Additional print 
statements were also added so that data on the location of the pump intake 
will always be written to the main listing file.

The program will not calculate corrections for partial penetration of a MNW2 well
if the losstype=SPECIFYcwc, in part because the required well radius is not 
specified in the input data for this losstype. If the input for a particular MNW2 
well specifies losstype=SPECIFYcwc and PPFLAG>0, the code will reset PPFLAG to a 
value of 0, and print a related warning message.

Code was added to check if the water table drops below the bottom of the open 
interval in a MNW2 node. If it did, that node is deactivated.

Problems related to the partial penetration correction calculation have been 
reported for MNW2 nodes in convertible cells. To minimize these, the PPFLAG is 
reset to 0 if the head in the well (hwell) declines to a level that only leaves 
less than 10% of the open interval saturated or if either hwell or the water table 
drops below the bottom of the open interval (in which case the node is also 
deactivated). 

A bug in the code for the case of a horizontal or slanted well and LOSSTYPE=GENERAL 
caused the code to ignore the specified value of "B" (the linear well-loss 
coefficient) and instead assumed that it was zero. This has been fixed. Note that 
the algorithm assumes that there is no directional dependence of B and that the 
specified value applies equally in all directions. This bug would have had only 
a very small effect on results in most cases.

Write statements were modified to help assure that elevations of well screens 
(open intervals) were printed correctly. Penetration fractions values will be 
printed as "N/A" for cases where partial penetration calculations are not made.

As described on p. 53 of the MNW2 documentation report (specifically, the last 
sentence describing both "QNDflag" and "QBHflag"), additional data will not be 
written if the well contains only one node. That is, both of these flags should 
be equal to 0 if the MNW well only includes a single node. If not, code added to 
the MNWI routines will detect this inconsistency and reset these flags to zero 
and also write an information message in the main output file when this triggering 
condition is found.

Several coding changes were made based on suggestions from Scott Boyce (CA WSC) 
and are labeled with his initials (seb).

Other minor format changes were made for the output files. 




Changes to the MNW2 Package for MODFLOW-2005 version 1.10.0   (Nov.-Dec. 2012)

A bug was fixed that affected simulations in which a composite well screen was 
generated when specifying multiple open intervals by elevation. In this case, 
some nodes were inadvertently excluded from the second interval. With the fix, 
all nodes of the multi-node well will be represented. Some output format 
adjustments were also made.

If a single-node multi-node well with a nonzero specified discharge were located 
in an inactive cell (IBOUND=0), it could generate a divide-by-zero error and 
halt execution of the program. The code was fixed to preclude such a 
floating-point error from occurring. A new warning message is now also written to 
the output file if this condition is detected.

If the well yield (and pumping rate) was reduced because of the seepage face 
calculations, an incorrect message (indicating erroneously that the cause was the 
head constraint) was written to the output file. The code was fixed so that 
possible causes of reduced puming rates are accurately printed.

The code was modified to eliminate separate processing for single-node MNW2 wells, 
which eliminated some inconsistencies in handling single-node wells. If the computed 
value for the head in single-node wells drops below the bottom of the cell, it invokes 
the seepage face calculation, which will reduce or eliminate the desired Q from the 
well. In cases where the Qdes is thereby reduced, the actual head in the well is 
indeterminate, but will be reported in separate MNWI output files as the limiting 
value of the bottom elevation of the cell together with an information note that the 
actual value may be lower than that reported value.  If Qdes is reduced to zero, the 
well is deactivated and that information is reported in the MNWI optional MNW2 
observation well file. 
 
At the end of the first paragraph on p. 32 of the documentation report, it states that 
the alternate calculations for CWC for nonvertical wells will be performed automatically 
when LOSSTYPE = THIEM, SKIN, or GENERAL. Unfortunately, the code did not check this 
condition, and erroneously performed these calculations when LOSSTYPE = SPECIFYCWC.  
The corrected code now uses the specified values of CWC for nonvertical wells when it 
is supposed to.

The code automatically estimates the maximum number of nodes (NODTOT) as required for 
allocation of arrays. However, if a large number of horizontal wells are being simulated, 
or possibly for other reasons, this default estimate proves to be inadequate, a new 
input option has been added to allow the user to directly specify a value for NODTOT. If 
this is a desired option, then it can be implemented by specifying a negative value for 
"MNWMAX"--the first value listed in Record 1 (Line 1) of the MNW2 input data file. If 
this is done, then the code will assume that the very next value on that line will be 
the desired value of "NODTOT". The model will then reset "MNWMAX" to its absolute value. 
The value of "IWL2CB" will become the third value on that line, etc.

The code included several coding errors in the calculation of cell-to-well conductances 
for nonvertical wells. There was also an error in the calculation of the length of closed 
casing between sequential, but non-adjacent, active nodes of a nonvertical MNW2 well (a 
value only used for informational purposes in the output file).  All of these errors have 
now been fixed. 


________________________________________________________________________________________

Changes to the MNW2 Package for MODFLOW-2005 version 1.9       (March, 2012)


A bug was fixed that affected simulations when both MNW2 and the HUF Package 
were used in the same simulation in conjunction with the partial penetration
correction. The variable KY is now declared as a Double Precision variable 
instead of being implicitly assumed (incorrectly) to be an Integer variable.  

A number of minor changes were made in Format statements to produce a cleaner 
output file.

In Subroutines GWF2MNW27BCF and GWF2MNW27HUF, corrections were made to assure 
the correct check is made for steady-state or transient conditions and to prevent 
a divide by zero error if a cell is dry. 

A bug was fixed for the calculation of angles theta and omega for slanted wells 
with an orientation into the southwest directional quadrant.



References

Konikow, L.F., Hornberger, G.Z., Halford, K.J., and Hanson, R.T., 2009,  
Revised multi-node well (MNW2) package for MODFLOW ground-water flow  
model: U.S. Geological Survey Techniques and Methods 6–A30, 67 p. 



