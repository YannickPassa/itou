
/* 
 
L'objectif est de créer une table agrégée sur les candidats et leur candidatures qui ne contient que les préscripteurs comme auteurs de diagnostics. 
Nous récupérons aussi différentes informations sur les structures à partir de la table organisation afin de mettre en place des filtres + précis

*/


with candidats as ( /* Ici on sélectionne les colonnes pertinentes à partir de la table candidats en ne prenant que les auteurs = Prescripteur */
    select  
        distinct cdd.id_anonymisé as id_candidat_anonymise, 
        cdd.actif as actif,   
        cdd.age as age,   
        cdd.date_dernière_connexion as date_derniere_connexion,   
        cdd.date_diagnostic as date_diagnostic, 
        cdd.département as departement,
        cdd.nom_département as nom_departement,
        cdd.région as region,
        cdd.type_auteur_diagnostic as type_auteur_diagnostic,
        cdd.sous_type_auteur_diagnostic as sous_type_auteur_diagnostic, 
        cdd.total_candidatures as total_candidatures, 
        cdd.total_diagnostics as total_diagnostics,
        cdd.total_embauches,
	 	cdd.type_inscription,
	    cdd.pe_inscrit
	from
		public.candidats as cdd /* cdd pour CanDiDats */
	where type_auteur_diagnostic = ('Prescripteur')
),

candidatures as ( /* Ici on sélectionne les colonnes pertinentes à partir de la table candidatures */
	select 
		cddr.id_candidat_anonymisé  as id_candidat_anonymise, 
		cddr.id_structure as id_structure,
		cddr.date_candidature, 
		cddr.date_embauche,
		cddr.département_structure,
		cddr.nom_département_structure,
		cddr.état,
		cddr.motif_de_refus,
		cddr.nom_org_prescripteur,
		cddr.nom_structure,
		cddr.origine,
		cddr.origine_détaillée,
		cddr.région_structure,
		cddr.type_structure,
		cddr.id_org_prescripteur	
	from
		public.candidatures as cddr /* cddr pour CanDiDatuRes */
),

organisations as ( /* On ne prend que type et type complet, le reste n'étant pas intéressant pour le moment */
	select 
		orga.id as id_structure,
		orga.type,
		orga.type_complet
	from 
		public.organisations as orga
)

select 
	*
from 
	candidats
		left join candidatures
			on candidats.id_candidat_anonymise = candidatures.id_candidat_anonymise  
		left join organisations 
			on candidatures.id_structure = organisations.id_structure
