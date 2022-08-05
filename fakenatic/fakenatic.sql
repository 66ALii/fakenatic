-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 04, 2022 at 10:37 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fakenatic`
--

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

CREATE TABLE `organization` (
  `ORG_ID` varchar(100) NOT NULL,
  `ORG_NAME` varchar(200) NOT NULL,
  `ORG_CONTACT` varchar(11) NOT NULL,
  `ORG_EMAIL` varchar(100) NOT NULL,
  `ORG_LOCATION` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `organization`
--

INSERT INTO `organization` (`ORG_ID`, `ORG_NAME`, `ORG_CONTACT`, `ORG_EMAIL`, `ORG_LOCATION`) VALUES
('ORG_asteria', 'asteria', '03313825756', 'asteria@gmail.com', 'gulshan'),
('ORG_szabist', 'szabist', '03313825756', 'szabist@gmail.com', 'clifton');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `U_ID` varchar(13) NOT NULL,
  `U_NAME` varchar(10) NOT NULL,
  `U_FULLNAME` varchar(100) NOT NULL,
  `U_EMAIL` varchar(100) NOT NULL,
  `U_CONTACT` varchar(11) NOT NULL,
  `U_PASSWD` varchar(255) NOT NULL,
  `ORG_ID` varchar(100) NOT NULL,
  `ROLE` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`U_ID`, `U_NAME`, `U_FULLNAME`, `U_EMAIL`, `U_CONTACT`, `U_PASSWD`, `ORG_ID`, `ROLE`) VALUES
('U_ali', 'ali', 'muhammad ali', 'ali@gmail.com', '03313825756', 'sha256$ydgMxMOL65Sx8i4c$27fc02b0a36be5c20e2c2b2c588d047273c6192ab35e6965d2ec8663110966a1', 'ORG_asteria', 'news anchor'),
('U_bisma', 'bisma', 'bisma arif', 'bisma@gmail.com', '03332302080', 'sha256$5rIj9avzBB4GOF93$7ff4a500d8419a0919f3deeab213d63991437597800823ca57cba830cbc68fae', 'ORG_szabist', 'news anchor');

-- --------------------------------------------------------

--
-- Table structure for table `video_catalog`
--

CREATE TABLE `video_catalog` (
  `video_id` varchar(100) NOT NULL,
  `user_id` varchar(100) NOT NULL,
  `video_url` varchar(255) NOT NULL,
  `audio_url` varchar(255) NOT NULL,
  `script_url` varchar(255) NOT NULL,
  `created_on` date NOT NULL,
  `created_by` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `video_catalog`
--

INSERT INTO `video_catalog` (`video_id`, `user_id`, `video_url`, `audio_url`, `script_url`, `created_on`, `created_by`) VALUES
('U_ali_1', 'U_ali', 'static/main\\U_ali/video/U_ali_vid1.mp4', 'static/main\\U_ali/audio/U_ali_aud1.mp3', '', '2022-06-15', 'ali'),
('U_ali_2', 'U_ali', 'static/main\\U_ali/video/U_ali_vid2.mp4', 'static/main\\U_ali/audio/U_ali_aud2.mp3', '', '2022-06-15', 'ali'),
('U_ali_3', 'U_ali', 'static/main\\U_ali/video/U_ali_vid3.mp4', 'static/main\\U_ali/audio/U_ali_aud3.mp3', '', '2022-06-16', 'ali');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `organization`
--
ALTER TABLE `organization`
  ADD PRIMARY KEY (`ORG_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`U_ID`);

--
-- Indexes for table `video_catalog`
--
ALTER TABLE `video_catalog`
  ADD PRIMARY KEY (`video_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
