-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Nov 15, 2024 alle 15:07
-- Versione del server: 10.6.18-MariaDB-0ubuntu0.22.04.1
-- Versione PHP: 8.1.2-1ubuntu2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `casilinaweb`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `regione`
--

CREATE TABLE `regione` (
  `cod_regione` int(11) NOT NULL,
  `nome_regione` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `regione`
--

INSERT INTO `regione` (`cod_regione`, `nome_regione`) VALUES
(5, 'Abruzzo'),
(6, 'Basilicata'),
(12, 'Calabria'),
(11, 'Campania'),
(16, 'Emilia-Romagna'),
(17, 'Friuli-Venezia Giulia'),
(10, 'Lazio'),
(18, 'Liguria'),
(2, 'Lombardia'),
(13, 'Marche'),
(15, 'Molise'),
(9, 'Piemonte'),
(8, 'Puglia'),
(4, 'Sardegna'),
(7, 'Sicilia'),
(3, 'Toscana'),
(19, 'Trentino-Alto Adige'),
(14, 'Umbria'),
(20, 'Valle d\'Aosta'),
(1, 'Veneto');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `regione`
--
ALTER TABLE `regione`
  ADD PRIMARY KEY (`cod_regione`),
  ADD UNIQUE KEY `nome_regione_indice` (`nome_regione`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
