-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2023 at 05:01 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_tbl`
--

CREATE TABLE `admin_tbl` (
  `admin_id` int(20) NOT NULL,
  `user_name` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_tbl`
--

INSERT INTO `admin_tbl` (`admin_id`, `user_name`, `password`) VALUES
(1, 'admin', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `student_tbl`
--

CREATE TABLE `student_tbl` (
  `student_id` int(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `contact` bigint(11) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `birth_date` date NOT NULL,
  `institutional_email` varchar(50) NOT NULL,
  `course` varchar(30) NOT NULL,
  `student_number` bigint(11) NOT NULL,
  `password` varchar(50) NOT NULL,
  `photo_path` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_tbl`
--

INSERT INTO `student_tbl` (`student_id`, `first_name`, `middle_name`, `last_name`, `contact`, `gender`, `birth_date`, `institutional_email`, `course`, `student_number`, `password`, `photo_path`, `status`) VALUES
(1, 'Diana', 'Fiel', 'Gonia', 9076765255, 'Female', '2002-11-24', 'diana.gonia@aclcbutuan.edu.ph', 'BS Information Technology', 21000497300, '1234', 'capture.png', 'active'),
(3, 'Marjore', 'Iglesias', 'Jamodiong', 9076765255, 'Female', '2003-05-04', 'marjore.jamodiong@aclcbutuan.edu.ph', 'BS Information Technology', 21000251530, '1234', 'marjore.png', 'active'),
(4, 'Daryll', 'Alingasa', 'Cabagay', 9076765255, 'Male', '1989-05-04', 'daryll.cabagay@aclcbutuan.edu.ph', 'BS Information Technology', 21000251520, '1234', 'daryll.jpg', 'active'),
(6, 'Haidee', 'Mercado', 'Yadao', 9305058209, 'Female', '2003-05-18', 'haidee.yadao@aclcbutuan.edu.ph', 'BS Information Technology', 21000251600, '1234', 'image_3.jpg', 'active'),
(7, 'Grace', 'Iglesias', 'Jamodiong', 9305058209, 'Female', '2003-05-04', 'grace.jamodiong@aclcbutuan.edu.ph', 'BS Information Technology', 21000251566, '1234', 'image_3.jpg', 'active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_tbl`
--
ALTER TABLE `admin_tbl`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `student_tbl`
--
ALTER TABLE `student_tbl`
  ADD PRIMARY KEY (`student_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_tbl`
--
ALTER TABLE `admin_tbl`
  MODIFY `admin_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `student_tbl`
--
ALTER TABLE `student_tbl`
  MODIFY `student_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
