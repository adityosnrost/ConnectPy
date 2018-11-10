-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 05, 2018 at 09:00 PM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 5.6.37

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eventsharelog`
--

-- --------------------------------------------------------

--
-- Table structure for table `emailshare`
--

CREATE TABLE `emailshare` (
  `id` int(7) NOT NULL,
  `filename` text NOT NULL,
  `email` text NOT NULL,
  `name` varchar(150) NOT NULL,
  `city` varchar(150) NOT NULL,
  `age` varchar(150) NOT NULL,
  `telephone` varchar(50) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `emailshare`
--

INSERT INTO `emailshare` (`id`, `filename`, `email`, `name`, `city`, `age`, `telephone`, `date`, `status`) VALUES
(9, 'd.jpg', 'adityosn@hotmail.com', 'Adityo', 'Jakarta', '18', '', '2018-10-04 18:50:30', 2),
(10, 'e.png', 'adityosn@hotmail.com', 'Adityo', 'Jakarta', '18', '', '2018-10-04 19:28:35', 2),
(11, 'e.png', 'adityosn@hotmail.com', 'Adityo', 'Jakarta', '18', '09837282817', '2018-10-05 18:58:27', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `emailshare`
--
ALTER TABLE `emailshare`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `emailshare`
--
ALTER TABLE `emailshare`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
