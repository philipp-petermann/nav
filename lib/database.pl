#!/usr/bin/perl -w

use Pg;
use strict;

sub db_hent {
    my ($db,$sql) = @_;
    return &db_select($db,$sql);
}
sub db_hent_hash {
    my ($db,$sql) = @_;
    my $res = &db_select($db,$sql);
    my %resultat;
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat{$_[0]} = [ @_ ];
    }
    return %resultat;
}
sub db_hent_hash_konkatiner {
    my ($db,$sql) = @_;
    my $res = &db_select($db,$sql);
    my %resultat;
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat{"$_[1]\/$_[2]"} = [ @_ ];
    }
    return %resultat;
}

sub db_hent_enkel {
    my ($db,$sql) = @_;
    my %resultat = ();
    my $res =  &db_select($db,$sql);
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat{$_[0]} = $_[1] ;
    }
    return %resultat;
}
sub db_hent_dobbel {
    my ($db,$sql) = @_;
    my %resultat = ();
    my $res =  &db_select($db,$sql);
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat{$_[0]}{$_[1]} = $_[2] ;
    }
    return %resultat;
}

sub db_select_hash {
    my $db = $_[0];
    my $tabell = $_[1];
    my @felt = @{$_[2]};
    my $en = $_[3];
    my $to = $_[4];
    my $tre = $_[5];

    my %resultat;
    my $sql = "SELECT ".join(",", @felt)." FROM $tabell";
    my $res =  &db_select($db,$sql);

    if(defined($tre)){
	while(@_ = $res->fetchrow) {
	    @_ = map rydd($_), @_;
	    $resultat{$_[$en]}{$_[$to]}{$_[$tre]} = [ @_ ] ;
	}
    } elsif (defined($to)) {
	while(@_ = $res->fetchrow) {
	    @_ = map rydd($_), @_;
	    $resultat{$_[$en]}{$_[$to]} = [ @_ ] ;
	}
    } elsif (defined($en)){
	while(@_ = $res->fetchrow) {
	    @_ = map rydd($_), @_;
	    $resultat{$_[$en]} = [ @_ ] ;
	}
    }
    return %resultat;
}





sub db_hent_dobbel_hash_konkatiner {
    my ($db,$sql) = @_;
    my %resultat = ();
    my $res =  &db_select($db,$sql);
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat{$_[1]}{$_[2]."/".$_[3]} = @_ ;
    }
    return %resultat;
}
sub db_hent_scalar {
    my ($db,$sql) = @_;
    my $resultat;
    my $res =  &db_select($db,$sql);
    while(@_ = $res->fetchrow) {
	@_ = map rydd($_), @_;
	$resultat = $_[1] ;
    }
    return $resultat;
}
sub db_sett_inn {
    my ($db,$tabell,$felt,$verdier) = @_;
    my @felt = split/:/,$felt;
    my @verdier = split/:/,$verdier;
    my @val;
    my @key;
    foreach my $i (0..$#felt) {
	if (defined($verdier[$i]) && $verdier[$i] ne ''){
	    #normal
	    push(@val, "\'".$verdier[$i]."\'");
	    push(@key, $felt[$i]);
#	} elsif (defined($verdier[$i])) {
	    #null
#	    push(@val, "NULL");
#	    push(@key, $felt[$i]);
	}
    }
    if(scalar(@key)){ #key eksisterer
	print "Setter inn *".join(" ",@val)."* i *$tabell*\n";
	my $sql = "INSERT INTO $tabell (".join(",",@key ).") VALUES (".join(",",@val).")";
#	print $sql,"\n";
	print &db_execute($db,$sql);
    }
}
sub db_insert {
    my $db = $_[0];
    my $tabell = $_[1];
    my @felt = @{$_[2]};
    my @verdier = @{$_[3]};

    my @val;
    my @key;
    foreach my $i (0..$#felt) {
	if (defined($verdier[$i]) && $verdier[$i] ne ''){
	    #normal
	    push(@val, "\'".$verdier[$i]."\'");
	    push(@key, $felt[$i]);
#	} elsif (defined($verdier[$i])) {
	    #null
#	    push(@val, "NULL");
#	    push(@key, $felt[$i]);
	}
    }
    if(scalar(@key)){ #key eksisterer
	my $nql = "SETTER INN I |$tabell| FELT |".join(" ",@key)."| VERDIER |".join(" ",@val)."|\n";
	my $sql = "INSERT INTO $tabell (".join(",",@key ).") VALUES (".join(",",@val).")";
	print "$nql\n";
	print &db_execute($db,$sql);
    }
}
sub db_update {
    my ($db,$tabell,$felt,$fra,$til,$hvor);
    unless($til eq $fra) {
	if ($til eq "" && $fra ne ""){
	    my $sql = "UPDATE $tabell SET $felt=null $hvor";
	    my $nql = "OPPDATERER |$tabell| FELT |$felt| FRA |$fra| TIL |null|\n";
	    print $nql;
	    print &db_execute($db,$sql);
	} else {
	    my $sql = "UPDATE $tabell SET $felt=\'$til\' $hvor";
	    my $nql = "OPPDATERER |$tabell| FELT |$felt| FRA |$fra| TIL |$til|\n";
	    print $nql;
	    print &db_execute($db,$sql);
	}
    }
}

sub db_oppdater {
    my ($db,$tabell,$felt,$fra,$til,$hvor_nokkel,$hvor_passer) = @_;

    print "Oppdaterer *$tabell* felt *$felt* fra *$fra* til *$til*\n";
    my $sql = "UPDATE $tabell SET $felt=$til WHERE $hvor_nokkel=\'$hvor_passer\'";
    print &db_execute($db,$sql);
#    print $sql,"\n";
}
sub db_oppdater_idant_to {
    my ($db,$tabell,$felt,$fra,$til,$hvor_nokkel1,$hvor_nokkel2,$hvor_passer1,$hvor_passer2) = @_;

    print "Oppdaterer *$tabell* felt *$felt* fra *$fra* til *$til*\n";
    my $sql = "UPDATE $tabell SET $felt=$til WHERE $hvor_nokkel1=\'$hvor_passer1\' AND $hvor_nokkel2=\'$hvor_passer2\'";
    print &db_execute($db,$sql);
#    print $sql,"\n";
}

sub db_delete {
    my ($db,$tabell,$hvor) = @_;
    my $nql =  "SLETTER FRA TABELL |$tabell| HVOR |$hvor|\n";
    my $sql = "DELETE FROM $tabell $hvor";
    print $nql;
    print &db_execute($db,$sql);
#    print $sql;
}    
sub db_slett {
    my ($db,$tabell,$hvor_nokkel,$hvor_passer) = @_;


    print "Sletter fra *$tabell* hvor $hvor_nokkel = $hvor_passer";
    my $sql = "DELETE FROM $tabell WHERE $hvor_nokkel=\'$hvor_passer\'";
    &db_execute($db,$sql);
    print $sql;
}    
sub db_slett_idant_to {
    my ($db,$tabell,$hvor_nokkel1,$hvor_nokkel2,$hvor_passer1,$hvor_passer2) = @_;


    print "Sletter fra *$tabell* hvor $hvor_nokkel1 = $hvor_passer1";
    my $sql = "DELETE FROM $tabell WHERE $hvor_nokkel1=\'$hvor_passer1\' AND $hvor_nokkel2=\'$hvor_passer2\'";
    &db_execute($db,$sql);
    print $sql;
}    

sub db_sletting{
    my $db = $_[0];
    my %ny = %{$_[1]};
    my %gammel = %{$_[2]};
    my @felt = @{$_[3]};
    my $tabell = $_[4];
#-----------------------------------
#DELETE
    #hvis den ikke ligger i fila
    for my $f (keys %gammel) {
	unless(exists($ny{$f})) {
	    &db_slett($db,$tabell,$felt[0],$f);
	}
    }
}

sub db_manipulate {
    my $db = $_[0];
    my $slett = $_[1];
    my $tabell = $_[2];
    my @felt = @{$_[3]};
    my @ny = @{$_[4]};
    my @gammel = @{$_[5]};
    my $en = $_[6];
    my $to = $_[7];
    my $tre = $_[8];

    my @where;

    if($en) {
	$where[0] = "$felt[1] = \'$en\' ";
    }
    if($to) {
	$where[1] = "$felt[2] = \'$to\' ";
    }
    if($tre) {
	$where[2] = "$felt[3] = \'$tre\' ";
    }

    my $where = " WHERE ".join("AND ",@where);

#	print "til: $ny[1] & fra: $gammel[1] $where\n";


    if($gammel[1]) {
	for my $i (0..$#felt ) {
	    if(defined( $gammel[$i] ) && defined( $ny[$i] )){
		&db_update($db,$tabell,@felt,$gammel[$i],$ny[$i],$where);

	    }
	}
    } else {
	&db_insert($db,$tabell,\@felt,\@ny);
    }

    if($slett == 1){
	unless($ny[1]) {
	    &db_delete($db,$tabell,$where);
	}
    }
}

#for fil og db-sammenlikning
sub db_endring_med_sletting {
    my ($db,$fil,$tabell,$felt) = @_;
    my @felt = split(/:/,$felt);
    my %ny = &fil_hent($fil,scalar(@felt));
    #leser fra database
    my %gammel = &db_hent_hash($db,"SELECT ".join(",", @felt )." FROM $tabell ORDER BY $felt[0]");
    &db_endring($db,\%ny,\%gammel,\@felt,$tabell);
    &db_sletting($db,\%ny,\%gammel,\@felt,$tabell);
}
#for fil og db-sammenlikning
sub db_endring_uten_sletting {
    my ($db,$fil,$tabell,$felt) = @_;
    my @felt = split(/:/,$felt);
    my %ny = &fil_hent($fil,scalar(@felt));
    #leser fra database
    my %gammel = &db_hent_hash($db,"SELECT ".join(",", @felt )." FROM $tabell ORDER BY $felt[0]");

    &db_endring($db,\%ny,\%gammel,\@felt,$tabell);
}
sub db_endring {

    my $db = $_[0];
    my %ny = %{$_[1]};
    my %gammel = %{$_[2]};
    my @felt = @{$_[3]};
    my $tabell = $_[4];
    for my $feltnull (keys %ny) {
	&db_endring_per_linje($db,\@{$ny{$feltnull}},\@{$gammel{$feltnull}},\@felt,$tabell,$feltnull);
    }
}

sub db_endring_per_linje {
    my $db = $_[0];
    my @ny = @{$_[1]};
    my @gammel = @{$_[2]};
    my @felt = @{$_[3]};
    my $tabell = $_[4];
    my $id = $_[5];
    
    #eksisterer i databasen?
    if($gammel[0]) {
#-----------------------
#UPDATE
	for my $i (0..$#felt ) {
	    if(defined( $gammel[$i] ) && defined( $ny[$i] )){
		unless($ny[$i] eq $gammel[$i]) {
		    #oppdatereringer til null m� ha egen sp�rring
		    if ($ny[$i] eq "" && $gammel[$i] ne ""){
			&db_oppdater($db,$tabell,$felt[$i],$gammel[$i],"null",$felt[0],$id);
		    } else {
			
			&db_oppdater($db,$tabell,$felt[$i],"\'$gammel[$i]\'","\'$ny[$i]\'",$felt[0],$id);
		    }
		}
	    }
	}
    }else{
#-----------------------
#INSERT
	&db_sett_inn($db,$tabell,join(":",@felt),join(":",@ny));
	
    }
}
sub db_alt_per_linje_idant_to {
    my $db = $_[0];
    my @ny = @{$_[1]};
    my @gammel = @{$_[2]};
    my @felt = @{$_[3]};
    my $tabell = $_[4];
    my $nokkel1 = $_[5];
    my $nokkel2 = $_[6];
    my $id1 = $_[7];
    my $id2 = $_[8];
    
    #eksisterer i databasen?
    if($gammel[0]) {
#-----------------------
#UPDATE
	for my $i (0..$#felt ) {
	    if(defined( $gammel[$i] ) && defined( $ny[$i] )){
		unless($ny[$i] eq $gammel[$i]) {
		    #oppdatereringer til null m� ha egen sp�rring
		    if ($ny[$i] eq "" && $gammel[$i] ne ""){
			&db_oppdater_idant_to($db,$tabell,$felt[$i],$gammel[$i],"null",$nokkel1,$nokkel2,$id1,$id2);
		    } else {
			
			&db_oppdate_idant_to($db,$tabell,$felt[$i],"\'$gammel[$i]\'","\'$ny[$i]\'",$nokkel1,$nokkel2,$id1,$id2);
		    }
		}
	    }
	}
    }else{
#-----------------------
#INSERT
	&db_sett_inn($db,$tabell,join(":",@felt),join(":",@ny));
	
    }
#-----------------------
#DELETE
    unless($ny[0]) {
	&db_slett_idant_to($db,$tabell,$nokkel1,$nokkel2,$id1,$id2);
    }
}
sub db_alt_per_linje {
    my $db = $_[0];
    my @ny = @{$_[1]};
    my @gammel = @{$_[2]};
    my @felt = @{$_[3]};
    my $tabell = $_[4];
    my $id = $_[5];
    
    #eksisterer i databasen?
    if($gammel[0]) {
#-----------------------
#UPDATE
	for my $i (0..$#felt ) {
	    if(defined( $gammel[$i] ) && defined( $ny[$i] )){
		unless($ny[$i] eq $gammel[$i]) {
		    #oppdatereringer til null m� ha egen sp�rring
		    if ($ny[$i] eq "" && $gammel[$i] ne ""){
			&db_oppdater($db,$tabell,$felt[$i],$gammel[$i],"null",$felt[0],$id);
		    } else {
			
			&db_oppdater($db,$tabell,$felt[$i],"\'$gammel[$i]\'","\'$ny[$i]\'",$felt[0],$id);
		    }
		}
	    }
	}
    }else{
#-----------------------
#INSERT
	&db_sett_inn($db,$tabell,join(":",@felt),join(":",@ny));
	
    }
#-----------------------
#DELETE
    unless($ny[0]) {
	&db_slett($db,$tabell,$felt[0],$id);
    }
}



sub rydd {    
    if (defined $_[0]) {
	$_ = $_[0];
	s/\s*$//;
	s/^\s*//;
    return $_;
    } else {
	return "";
    }
}
sub db_connect {
    my ($db,$user,$password) = @_;
    my $conn = Pg::connectdb("dbname=$db user=$user password=$password");
    die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;
    return $conn;
}
sub db_select {
    my $sql = $_[1];
    my $conn = $_[0];
    my $resultat = $conn->exec($sql);
    die "KLARTE IKKE � SP�RRE: \n$sql\n".$conn->errorMessage
	unless ($resultat->resultStatus eq PGRES_TUPLES_OK);
    return $resultat;
}
sub db_execute {
    my $sql = $_[1];
    my $conn = $_[0];
    my $resultat = $conn->exec($sql);
    print "DATABASEFEIL: \n$sql\n".$conn->errorMessage
	unless ($resultat->resultStatus eq PGRES_COMMAND_OK);
    return $resultat->oidStatus;
}

return 1;
