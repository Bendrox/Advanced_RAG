# Advanced-RAG

### Checklist pour un Projet RAG lvl 1 :   
1.	Définition des Objectifs
	•	Identifier clairement les cas d ’utilisation et les objectifs du projet.

2.	Collecte et Préparation des Données
	•	Rassembler les sources de données pertinentes (documents, bases de données, etc.).
	•	Nettoyer et prétraiter les données pour assurer leur qualité.

3.	Indexation des Données
	•	Convertir les données en vecteurs à l’aide de modèles d’embeddings appropriés.
	•	Stocker ces vecteurs dans une base de données vectorielle pour une récupération efficace.

4.	Sélection du Modèle de Langage
	•	Choisir un modèle de langage adapté aux besoins du projet.

5.	Intégration du Système de Récupération
	•	Mettre en place un système capable de récupérer les informations pertinentes en fonction des requêtes des utilisateurs.

6.	Pipeline de Génération
	•	Développer un pipeline qui intègre les informations récupérées dans le modèle de langage pour générer des réponses pertinentes.

7.	Évaluation et Tests
	•	Tester le système pour s’assurer de sa précision et de sa pertinence.
	•	Recueillir les retours des utilisateurs pour des améliorations continues.


### Checklist pour un Projet RAG lvl 2 - advanced: 
1.	Amélioration de la Qualité des Données
	•	Mettre en place des processus pour garantir la fraîcheur et la diversité des données.
	•	Utiliser des techniques d’augmentation de données pour enrichir le corpus.

2.	Optimisation du Composant de Récupération
	•	Évaluer et améliorer la vitesse et la précision du processus de récupération.
	•	Mettre en œuvre des techniques de réécriture de requêtes et de reranking pour améliorer les résultats.

3.	Amélioration du Composant de Génération
	•	Assurer la cohérence et la pertinence des réponses générées.
	•	Intégrer des mécanismes pour éviter les “hallucinations” du modèle.

4.	Techniques Avancées
	•	Auto-Réflexion (Slf-Reflective RAG) : Permettre au modèle d’évaluer de manière autonome la nécessité d’informatios externes et la qualité de ses réponses.
	•	RAG Correctif (Corrective RAG) : Évaluer la qualité des documents récupérés et décider de leur utilisation ou de la nécessité de recherches supplémentaires.
	•	Fusion RAG (RAG Fusion) : Générer des requêtes dérivées et combiner les documents récupérés pour fournir des réponses plus complètes.

5.	Évaluation Continue et Optimisation
	•	Metre en place des protocoles d’évaluation pour mesurer la précision, la pertinence et la satisfaction des utilisateurs.
	•	Optimiser les performances en surveillant les temps de latence et l’utilisation des ressources.


Réaliser un benchmark des modèles d'embedding open source.
Collecter et préparer des données adaptées.
Automatiser la génération du dataset pour l'entraînement.
Effectuer un further finetuning du modèle.
Évaluer les performances avec :

Les données spécifiques de la Banque de France.
Le benchmark MTEB pour une évaluation standardisée.
