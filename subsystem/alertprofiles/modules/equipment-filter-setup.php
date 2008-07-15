<?php
/*
 *
 * Copyright 2002-2004 UNINETT AS
 * 
 * This file is part of Network Administration Visualized (NAV)
 *
 * NAV is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * NAV is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NAV; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 *
 * Authors: Andreas Aakre Solberg <andreas.solberg@uninett.no>
 *
 */
?><table width="100%" class="mainWindow">
<tr><td class="mainWindowHead">
<?php
echo '<p>Filter setup</p>';
if ( get_exist('fid') ) {
	session_set('match_fid', get_get('fid') );
}
$utstginfo = $dbh->utstyrfilterInfo( session_get('match_fid') );
echo '<div class="subheader">' . $utstginfo[0] . '</div>';

?>

</td></tr>

<tr><td>
<?php
include("loginordie.php");
loginOrDie();


echo '<p>' . gettext("A filter consist of one (or more) expressions of the following form:") . 
	'<br>' . gettext('Filter = &lt;variable&gt; &lt;selection criteria&gt; &lt;value&gt;') . '<br>' . 
	gettext('If <b>one or more</b> of the filter expressions fail to match the alert in 
question, no alarm will be sent.') . '<p>' .
	gettext('Please note that the set of variables used to compose filters may
be expanded by the NAV administrator.');



$dbhk = $dbinit->get_dbhk();
$brukernavn = session_get('bruker'); $uid = session_get('uid');

if ( session_get('admin') < 100 && !$dbh->permissionEquipmentFilter( session_get('uid'), session_get('match_fid') ) ) {
	echo "<h2>Security violation</h2>";
	exit(0);
}


if (isset($subaction) && $subaction == 'slett') {
	if (session_get('match_fid') > 0) { 
		$dbh->slettFiltermatch(session_get('match_fid'), get_get('mid') );
		print "<p><font size=\"+3\">" . gettext("OK</font>, the expression is removed from the filter.");
	} else {
		print "<p><font size=\"+3\">" . gettext("An error</font> occured, the expression is <b>not</b> removed.");
	}
}


if (isset($subaction) && $subaction == "nymatch") {
	print "<h3>" . gettext("Registering new expression...") . "</h3>";
	
	if ($uid > 0) {
	
		if (post_get('matchtype') == 11) {

			if (post_exist('mverdi')) {
				$tval = implode('|', post_get('mverdi'));
				//print "<p>Values:$tval";
				$matchid = $dbh->nyMatch(post_get('matchfelt'), post_get('matchtype'), 
					$tval, session_get('match_fid') );				
			} else if (post_exist('verdi')) {
				$tval = implode('|', explode(' ', post_get('verdi')));
				$matchid = $dbh->nyMatch(post_get('matchfelt'), post_get('matchtype'), 
					$tval, session_get('match_fid') );				
			} else {
				print "<p><font size=\"+3\">" . gettext("No values selected, a new expression is <b>not</b> added.");
			}
		} else {
			$matchid = $dbh->nyMatch(post_get('matchfelt'), post_get('matchtype'), 
			post_get('verdi'), session_get('match_fid') );
		}
		print "<p><font size=\"+3\">" . gettext("OK</font>, a new expression (match) is added to this filter.");
	
	} else {
		print "<p><font size=\"+3\">" . gettext("An error</font> occured, a new expression is  <b>not</b> added.");
	}
	$subaction = "";
	unset($matchfelt);
}


$l = new Lister(111,
    array(gettext('Field'), gettext('Condition'), gettext('Value'), gettext('Option..') ),
    array(40, 15, 25, 10),
    array('left', 'left', 'left', 'left'),
    array(true, true, true, false),
    0
);


//print "<h3>" . gettext("Filter matches") . "</h3>";
print "<p>";

if ( get_exist('sortid') )
	$l->setSort(get_get('sort'), get_get('sortid') );
	
$match = $dbh->listMatch(session_get('match_fid'), $l->getSort() );

for ($i = 0; $i < sizeof($match); $i++) {
	$valg = '<a href="index.php?action=match&subaction=slett&mid=' . 
		$match[$i][0] . '">' .
		'<img alt="Delete" src="icons/delete.gif" border=0>' .
		'</a>';
	
	$l->addElement( array(
		$match[$i][1],  // felt
		$type[$match[$i][2]], // type
		$match[$i][3], // verdi
		$valg ) 
	);
}

print $l->getHTML();

print "<p>[ <a href=\"index.php?action=match\">" . gettext("update") . " <img src=\"icons/refresh.gif\" class=\"refresh\" alt=\"oppdater\" border=0> ]</a> ";
print "Antall filtermatcher: " . sizeof($match);


echo '<a name="nymatch"></a><div class="newelement"><h3>';
echo gettext("Add new expression");
echo '</h3>';



print '<form name="form1" method="post" action="index.php?action=match&subaction=velgmatchfelt">';

?>
  <table width="100%" border="0" cellspacing="0" cellpadding="3">


    <tr>
    	<td width="30%"><p><?php echo gettext('Variable'); ?></p></td>
    	<td width="70%">
    	<select name="matchfelt" id="select" onChange="this.form.submit()">
<?php

// Viser oversikt over hvilke filtermatchfelter man kan velge...
$matchfields = $dbh->listMatchField(1);

foreach ($matchfields AS $matchfield) {
	$sel = "";
	if ($matchfield[0] == best_get('matchfelt')) { $sel = " selected"; }
	print '<option value="' . $matchfield[0] . '"' . $sel . '>' . $matchfield[1] . '</option>';
}

echo '</select></td></tr>';


echo '</form><form name="nymatch" method="post" action="index.php?action=match&subaction=velgoperator">';

if ( post_exist('matchfelt') ) {
	$valgt_matchfelt = post_get('matchfelt');
} else {
	$valgt_matchfelt = $matchfields[0][0];
}
//echo '<p>Valg matchfelt er: ' . $valgt_matchfelt . ' postverdi er:' .  post_get('matchfelt');
/*
	$mf[0] = $data["name"];
	$mf[1] = $data["descr"];
	$mf[2] = $data["valuehelp"];
	$mf[3] = $data["valueid"];
	$mf[4] = $data["valuename"];
	$mf[5] = $data["valuecategory"];
	$mf[6] = $data["valuesort"];
	$mf[7] = $data["listlimit"];
	$mf[8] = $data["showlist"];
*/

$matchfieldinfo = $dbh->matchFieldInfo($valgt_matchfelt);

echo '<tr><td colspan="2"><small><p>';
echo $matchfieldinfo[1];
echo '</small></td></tr>';



echo '<tr>';


// Valg av operator ----------------------------------------


if ( post_exist('matchtype') ) {
	$valgt_matchtype = post_get('matchtype');
} else {
	$valgt_matchtype = $matchfieldinfo[9][0];
}
//echo '<p>Valg matchtype er: ' . $valgt_matchtype . ' postverdi er:' .  post_get('matchtype');


echo '<td width="30%"><p>';
echo gettext("Selection criteria");
echo '</p></td><td width="70%">';

echo '<input type="hidden" name="matchfelt" value="' . $valgt_matchfelt . '">';

print '<select name="matchtype" id="select" onChange="this.form.submit()">';

if ( sizeof($matchfieldinfo[9]) > 0) {
	foreach ($matchfieldinfo[9] as $matchtype) {
		$selected = "";
		if ($matchtype == $valgt_matchtype) { $selected = " selected";   }
		print '<option value="' . $matchtype . '"' . $selected . '>' . $type[$matchtype] . '</option>';
	}
} else {
	print '<option value="0" selected>' . gettext("equals") . '</option>';	
}
echo '</select>';
echo '</td></tr>';
echo '<tr><td colspan="2"><small><p>';
echo $matchfieldinfo[2];
echo '</small></td></tr>';








echo '</form><form name="nymatch" method="post" action="index.php?action=match&subaction=nymatch">';
echo '<input type="hidden" name="matchfelt" value="' . $valgt_matchfelt . '">';
echo '<input type="hidden" name="matchtype" value="' . $valgt_matchtype . '">';
?>
   	
    <tr>     
    	<td width="30%"><p><?php echo gettext('Set value'); ?></p></td>
    	<td width="70%">
<?php    




// Valg av verdi ----------------------------------------	

if ($matchfieldinfo[8] == 't' ) {

	$verdier = $dbhk->listVerdier(
		$matchfieldinfo[3],
		$matchfieldinfo[4],
		$matchfieldinfo[5],
		$matchfieldinfo[6],
		$matchfieldinfo[7]
	);  
  
  
	if ($valgt_matchtype == 11) {
		echo '<select name="mverdi[]" id="select" style="width: 100%" size="15" multiple>';    
		ksort($verdier);
		// Traverser kategorier
		foreach ($verdier AS $cat => $catlist) {
			if ($cat != "") echo '<optgroup label="' . $cat . '">';
			foreach ($catlist AS $catelem) {
				echo ' <option value="' . $catelem[0] . '">' . $catelem[1] . '</option>' . "\n";
			}
			if ($cat != "") echo '</optgroup>';
		}
		echo '</select>';	
	} else {	
		echo '<select name="verdi" id="select">';    
		ksort($verdier);
		// Traverser kategorier
		foreach ($verdier AS $cat => $catlist) {
			if ($cat != "") echo '<optgroup label="' . $cat . '">';
			foreach ($catlist AS $catelem) {
				echo ' <option value="' . $catelem[0] . '">' . $catelem[1] . '</option>' . "\n";
			}
			if ($cat != "") echo '</optgroup>';
		}
		echo '</select>';
	}		
	
	
	
} else {
	echo '<input name="verdi" size="40">';
}    

?>

        </td></tr>



    <tr>
      <td>&nbsp;</td>
      
<?php

$tekst = gettext("Add expression");

print '<td><input type="submit" name="Submit" value="' . $tekst . '"></td>';



?>
    </tr>
  </table>

</form></div>

<?php
	echo '<div align="right"><form name="finnished" method="post" action="index.php?action=' . session_get('lastaction') . '">';
	echo '<input type="submit" name="Submit" value="' . gettext('Finished setting up filter') . '">';
	echo '</form></div>';
?>

</td></tr>
</table>
