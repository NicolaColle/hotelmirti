-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Nov 15, 2024 alle 15:53
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
-- Database: `hotel_mirti`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `stato`
--

CREATE TABLE `stato` (
  `cod_stato` int(11) NOT NULL,
  `nome_stato` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `stato`
--

INSERT INTO `stato` (`cod_stato`, `nome_stato`) VALUES
(1, 'Afghanistan'),
(2, 'Åland Islands'),
(3, 'Albania'),
(4, 'Algeria'),
(5, 'American Samoa'),
(6, 'Andorra'),
(7, 'Angola'),
(8, 'Anguilla'),
(9, 'Antarctica'),
(10, 'Antigua and Barbuda'),
(11, 'Argentina'),
(12, 'Armenia'),
(13, 'Aruba'),
(14, 'Australia'),
(15, 'Austria'),
(16, 'Azerbaijan'),
(17, 'Bahamas'),
(18, 'Bahrain'),
(19, 'Bangladesh'),
(20, 'Barbados'),
(21, 'Belarus'),
(22, 'Belgium'),
(23, 'Belize'),
(24, 'Benin'),
(25, 'Bermuda'),
(26, 'Bhutan'),
(27, 'Bolivia (Plurinational State of)'),
(28, 'Bonaire, Sint Eustatius and Saba'),
(29, 'Bosnia and Herzegovina'),
(30, 'Botswana'),
(31, 'Bouvet Island'),
(32, 'Brazil'),
(33, 'British Indian Ocean Territory'),
(34, 'Brunei Darussalam'),
(35, 'Bulgaria'),
(36, 'Burkina Faso'),
(37, 'Burundi'),
(38, 'Cabo Verde'),
(39, 'Cambodia'),
(40, 'Cameroon'),
(41, 'Canada'),
(42, 'Cayman Islands'),
(43, 'Central African Republic'),
(44, 'Chad'),
(45, 'Chile'),
(46, 'China'),
(47, 'Colombia'),
(48, 'Comoros'),
(49, 'Congo'),
(50, 'Congo (Democratic Republic of the)'),
(51, 'Cook Islands'),
(52, 'Costa Rica'),
(53, 'Croatia'),
(54, 'Cuba'),
(55, 'Curaçao'),
(56, 'Cyprus'),
(57, 'Czech Republic'),
(58, 'Denmark'),
(59, 'Djibouti'),
(60, 'Dominica'),
(61, 'Dominican Republic'),
(62, 'Ecuador'),
(63, 'Egypt'),
(64, 'El Salvador'),
(65, 'Equatorial Guinea'),
(66, 'Eritrea'),
(67, 'Estonia'),
(68, 'Eswatini'),
(69, 'Ethiopia'),
(70, 'Falkland Islands (Malvinas)'),
(71, 'Faroe Islands'),
(72, 'Fiji'),
(73, 'Finland'),
(74, 'France'),
(75, 'French Guiana'),
(76, 'French Polynesia'),
(77, 'French Southern Territories'),
(78, 'Gabon'),
(79, 'Gambia'),
(80, 'Georgia'),
(81, 'Germany'),
(82, 'Ghana'),
(83, 'Gibraltar'),
(84, 'Greece'),
(85, 'Greenland'),
(86, 'Grenada'),
(87, 'Guadeloupe'),
(88, 'Guam'),
(89, 'Guatemala'),
(90, 'Guinea'),
(91, 'Guinea-Bissau'),
(92, 'Guyana'),
(93, 'Haiti'),
(94, 'Heard Island and McDonald Islands'),
(95, 'Honduras'),
(96, 'Hong Kong'),
(97, 'Hungary'),
(98, 'Iceland'),
(99, 'India'),
(100, 'Indonesia'),
(101, 'Iran'),
(102, 'Iraq'),
(103, 'Ireland'),
(104, 'Isle of Man'),
(105, 'Israel'),
(106, 'Italy'),
(107, 'Jamaica'),
(108, 'Japan'),
(109, 'Jordan'),
(110, 'Kazakhstan'),
(111, 'Kenya'),
(112, 'Kiribati'),
(113, 'Korea (North)'),
(114, 'Korea (South)'),
(115, 'Kuwait'),
(116, 'Kyrgyzstan'),
(117, 'Lao People\'s Democratic Republic'),
(118, 'Latvia'),
(119, 'Lebanon'),
(120, 'Lesotho'),
(121, 'Liberia'),
(122, 'Libya'),
(123, 'Liechtenstein'),
(124, 'Lithuania'),
(125, 'Luxembourg'),
(126, 'Macao'),
(127, 'North Macedonia'),
(128, 'Madagascar'),
(129, 'Malawi'),
(130, 'Malaysia'),
(131, 'Maldives'),
(132, 'Mali'),
(133, 'Malta'),
(134, 'Marshall Islands'),
(135, 'Martinique'),
(136, 'Mauritania'),
(137, 'Mauritius'),
(138, 'Mayotte'),
(139, 'Mexico'),
(140, 'Micronesia (Federated States of)'),
(141, 'Moldova'),
(142, 'Monaco'),
(143, 'Mongolia'),
(144, 'Montenegro'),
(145, 'Montserrat'),
(146, 'Morocco'),
(147, 'Mozambique'),
(148, 'Myanmar'),
(149, 'Namibia'),
(150, 'Nauru'),
(151, 'Nepal'),
(152, 'Netherlands'),
(153, 'New Caledonia'),
(154, 'New Zealand'),
(155, 'Nicaragua'),
(156, 'Niger'),
(157, 'Nigeria'),
(158, 'Niue'),
(159, 'Norway'),
(160, 'Oman'),
(161, 'Pakistan'),
(162, 'Palau'),
(163, 'Palestine'),
(164, 'Panama'),
(165, 'Papua New Guinea'),
(166, 'Paraguay'),
(167, 'Peru'),
(168, 'Philippines'),
(169, 'Pitcairn'),
(170, 'Poland'),
(171, 'Portugal'),
(172, 'Puerto Rico'),
(173, 'Qatar'),
(174, 'Republic of Kosovo'),
(175, 'Réunion'),
(176, 'Romania'),
(177, 'Russian Federation'),
(178, 'Rwanda'),
(179, 'Saint Kitts and Nevis'),
(180, 'Saint Lucia'),
(181, 'Saint Vincent and the Grenadines'),
(182, 'Samoa'),
(183, 'San Marino'),
(184, 'Sao Tome and Principe'),
(185, 'Saudi Arabia'),
(186, 'Senegal'),
(187, 'Serbia'),
(188, 'Seychelles'),
(189, 'Sierra Leone'),
(190, 'Singapore'),
(191, 'Sint Maarten'),
(192, 'Slovakia'),
(193, 'Slovenia'),
(194, 'Solomon Islands'),
(195, 'Somalia'),
(196, 'South Africa'),
(197, 'South Georgia and the South Sandwich Islands'),
(198, 'South Sudan'),
(199, 'Spain'),
(200, 'Sri Lanka'),
(201, 'Sudan'),
(202, 'Suriname'),
(203, 'Sweden'),
(204, 'Switzerland'),
(205, 'Syrian Arab Republic'),
(206, 'Taiwan'),
(207, 'Tajikistan'),
(208, 'Tanzania'),
(209, 'Thailand'),
(210, 'Timor-Leste'),
(211, 'Togo'),
(212, 'Tokelau'),
(213, 'Tonga'),
(214, 'Trinidad and Tobago'),
(215, 'Tunisia'),
(216, 'Turkey'),
(217, 'Turkmenistan'),
(218, 'Tuvalu'),
(219, 'Uganda'),
(220, 'Ukraine'),
(221, 'United Arab Emirates'),
(222, 'United Kingdom'),
(223, 'United States of America'),
(224, 'Uruguay'),
(225, 'Uzbekistan'),
(226, 'Vanuatu'),
(227, 'Holy See (Vatican City State)'),
(228, 'Venezuela'),
(229, 'Viet Nam'),
(230, 'Virgin Islands (British)'),
(231, 'Virgin Islands (U.S.)'),
(232, 'Western Sahara'),
(233, 'Yemen'),
(234, 'Zambia'),
(235, 'Zimbabwe');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `stato`
--
ALTER TABLE `stato`
  ADD PRIMARY KEY (`cod_stato`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `stato`
--
ALTER TABLE `stato`
  MODIFY `cod_stato` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=236;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
