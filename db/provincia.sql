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
-- Struttura della tabella `provincia`
--

CREATE TABLE `provincia` (
  `cod_provincia` int(11) NOT NULL,
  `nome_provincia` varchar(100) DEFAULT NULL,
  `cod_regione` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `provincia`
--

INSERT INTO `provincia` (`cod_provincia`, `nome_provincia`, `cod_regione`) VALUES
(1, 'Padova', 1),
(2, 'Lodi', 2),
(3, 'Lecco', 2),
(4, 'Siena', 3),
(5, 'Oristano', 4),
(6, 'Pescara', 5),
(7, 'Milano', 2),
(8, 'Pistoia', 3),
(9, 'Potenza', 6),
(10, 'Ragusa', 7),
(11, 'Foggia', 8),
(12, 'Cuneo', 9),
(13, 'Matera', 6),
(14, 'L\'Aquila', 5),
(15, 'Rieti', 10),
(16, 'Salerno', 11),
(17, 'Napoli', 11),
(18, 'Catania', 7),
(19, 'Frosinone', 10),
(20, 'Cosenza', 12),
(21, 'Brescia', 2),
(22, 'Pesaro e Urbino', 13),
(23, 'Cremona', 2),
(24, 'Mantova', 2),
(25, 'Viterbo', 10),
(26, 'Vibo Valentia', 12),
(27, 'Ascoli Piceno', 13),
(28, 'Terni', 14),
(29, 'Campobasso', 15),
(30, 'Isernia', 15),
(31, 'Bari', 8),
(32, 'Caltanissetta', 7),
(33, 'Messina', 7),
(34, 'Alessandria', 9),
(35, 'Bergamo', 2),
(36, 'Rovigo', 1),
(37, 'Verona', 1),
(38, 'Roma', 10),
(39, 'Reggio Calabria', 12),
(40, 'Piacenza', 16),
(41, 'Sassari', 4),
(42, 'Enna', 7),
(43, 'Asti', 9),
(44, 'Torino', 9),
(45, 'Belluno', 1),
(46, 'Varese', 2),
(47, 'Monza e della Brianza', 2),
(48, 'Novara', 9),
(49, 'Agrigento', 7),
(50, 'Ancona', 13),
(51, 'Vicenza', 1),
(52, 'Udine', 17),
(53, 'Avellino', 11),
(54, 'Caserta', 11),
(55, 'Biella', 9),
(56, 'Benevento', 11),
(57, 'Imperia', 18),
(58, 'Trento', 19),
(59, 'Pavia', 2),
(60, 'Vercelli', 9),
(61, 'Savona', 18),
(62, 'Teramo', 5),
(63, 'Sondrio', 2),
(64, 'Parma', 16),
(65, 'Como', 2),
(66, 'Catanzaro', 12),
(67, 'Reggio Emilia', 16),
(68, 'Trapani', 7),
(69, 'Bolzano', 19),
(70, 'Lecce', 8),
(71, 'Ravenna', 16),
(72, 'Palermo', 7),
(73, 'Aosta', 20),
(74, 'Fermo', 13),
(75, 'Chieti', 5),
(76, 'Treviso', 1),
(77, 'Lucca', 3),
(78, 'Bologna', 16),
(79, 'Spezia', 18),
(80, 'Pordenone', 17),
(81, 'Barletta-Andria-Trani', 8),
(82, 'Arezzo', 3),
(83, 'Venezia', 1),
(84, 'Verbano-Cusio-Ossola', 9),
(85, 'Macerata', 13),
(86, 'Latina', 10),
(87, 'Sud Sardegna', 4),
(88, 'Grosseto', 3),
(89, 'Genova', 18),
(90, 'Ferrara', 16),
(91, 'Nuoro', 4),
(92, 'Cagliari', 4),
(93, 'Perugia', 14),
(94, 'Siracusa', 7),
(95, 'Massa-Carrara', 3),
(96, 'Taranto', 8),
(97, 'Firenze', 3),
(98, 'Forlì-Cesena', 16),
(99, 'Modena', 16),
(100, 'Rimini', 16),
(101, 'Crotone', 12),
(102, 'Livorno', 3),
(103, 'Pisa', 3),
(104, 'Brindisi', 8),
(105, 'Prato', 3),
(106, 'Gorizia', 17),
(107, 'Trieste', 17);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `provincia`
--
ALTER TABLE `provincia`
  ADD PRIMARY KEY (`cod_provincia`),
  ADD UNIQUE KEY `nome_provincia_indice` (`nome_provincia`) USING BTREE,
  ADD KEY `cod_regione` (`cod_regione`);

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `provincia`
--
ALTER TABLE `provincia`
  ADD CONSTRAINT `provincia_ibfk_1` FOREIGN KEY (`cod_regione`) REFERENCES `regione` (`cod_regione`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
