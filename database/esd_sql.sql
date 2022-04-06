SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `ESD` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ESD`;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` INT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE user AUTO_INCREMENT=1000;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `email`, `password`) VALUES
('yixin', 'yixin@mail.com', 'password'), 
('kokwee', 'kokwee@mail.com', 'password'),
('biondi', 'biondi@mail.com', 'password'),
('jianlin', 'jianlin@mail.com', 'password'),
('joel', 'joel@mail.com', 'password');
COMMIT;

DROP TABLE IF EXISTS `hawker`;
CREATE TABLE IF NOT EXISTS `hawker` (
  `hawker_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet_id` INT DEFAULT NULL,
  `cuisine` varchar(64) NOT NULL,
  `halal` BOOLEAN DEFAULT FALSE,
  `has_vegetarian_option` BOOLEAN DEFAULT FALSE,
  `opening_hours` time(6) DEFAULT '07:00:00',
  `closing_hours` time(6) DEFAULT '20:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE hawker AUTO_INCREMENT=2000;

--
-- Dumping data for table `user`
--

INSERT INTO `hawker` (`username`, `email`, `password`, `opening_hours`, `closing_hours`) VALUES
('chinese', 'chinese@mail.com', 'password', '09:00:00', '21:00:00'), 
('muslim', 'muslim@mail.com', 'password', '08:00:00', '22:00:00'),
('vegetarian', 'vegetarian@mail.com', 'password', '07:30:00', '19:00:00'),
('japanese', 'japanese@mail.com', 'password', '07:30:00', '19:00:00'),
('korean', 'korean@mail.com', 'password', '10:00:00', '20:00:00'),
('indian', 'indian@mail.com', 'password', '10:00:00', '20:00:00');
COMMIT;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `item_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `hawker_id` INT NOT NULL,
  `name` varchar(64) NOT NULL,
  `cuisine` varchar(64) NOT NULL,
  `description` varchar(255) NOT NULL,
  `course` varchar(64) NOT NULL,
  `price` float NOT NULL,
  `vegetarian` BOOLEAN DEFAULT FALSE,
  `available` BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE item AUTO_INCREMENT=3000;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`hawker_id`, `name`, `description`, 
`price`, `cuisine`, `course`, `vegetarian`, `available`) VALUES
(2000, 'chicken rice', 'this is chicken and rice', 3.8, 'chinese', 'main', FALSE, TRUE), 
(2000, 'chinese rojak', 'this is fruit and vege rojak', 4.9, 'chinese', 'side', TRUE, TRUE), 

(2001, 'nasi lemak', 'this is nasi lemak', 4.9, 'muslim', 'main', FALSE, TRUE), 
(2001, 'satay', 'meat on stick yum', 0.5, 'muslim', 'side', FALSE, TRUE), 

(2002, 'popiah', 'spring roll', 3.0, 'vegetarian', 'side', TRUE, TRUE), 
(2002, 'bee hoon', 'this is bee hoon', 4.3, 'vegetarian', 'main', TRUE, TRUE), 

(2003, 'oyakodon', 'OYAKODONNNN', 4.9, 'japanese', 'main', FALSE, TRUE), 
(2003, 'takoyaki', 'octopus balls bussin', 3.9, 'japanese', 'side', FALSE, TRUE), 

(2004, 'bibimbap', 'rice and many vege and sauce yum', 5.3, 'korean', 'main', TRUE, FALSE),
(2004, 'soju', 'sweet drink slurp', 12, 'korean', 'drink', TRUE, FALSE), -- haram SIAL

(2005, 'maggi goreng', 'best supper dish', 4.9, 'indian', 'main', FALSE, FALSE),
(2005, 'milo tower', 'best of the best no cap', 30.0, 'indian', 'drink', TRUE, FALSE);

COMMIT;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `order_id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `hawker_id` INT NOT NULL,
  `status` varchar(16) NOT NULL,
  `total_price` float NOT NULL,
  `discount` float NOT NULL,
  `final_price` float NOT NULL,
  `items` varchar(255) NOT NULL,
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `order` AUTO_INCREMENT=4000;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`user_id`, `hawker_id`, `status`, `total_price`, `discount`, `final_price`, `items`) VALUES
(1000, 2000, "pending", 12.5, 0, 12.5, "[{'item_id': 3000, 'quantity': 2}, {'item_id': 3001, 'quantity': 1}]"),
(1000, 2001, "accepted", 19.8, 0.8, 19, "[{'item_id': 3002, 'quantity': 2}, {'item_id': 3003, 'quantity': 20}]");
COMMIT;

--
-- Table structure for table `wallet`
--

DROP TABLE IF EXISTS `wallet`;
CREATE TABLE IF NOT EXISTS `wallet` (
  `wallet_id` INT PRIMARY KEY,
  `total_balance` float NOT NULL,
  `available_balance` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `wallet`
--

INSERT INTO `wallet` (`wallet_id`, `total_balance`, `available_balance`) VALUES
(1000, 81.5, 50),
(1001, 100.0, 100.0),
(1002, 80.0, 80.0),
(1003, 20, 20.0),
(1004, 0.0, 0.0),
(2000, 0, 0),
(2001, 0, 0),
(2002, 0, 0),
(2003, 0, 0),
(2004, 0, 0),
(2005, 0, 0);
COMMIT;

--
-- Table structure for table `escrow`
--

DROP TABLE IF EXISTS `escrow`;
CREATE TABLE IF NOT EXISTS `escrow` (
  `order_id` INT PRIMARY KEY,
  `payer_id` INT NOT NULL,
  `receiving_id` INT NOT NULL,
  `amount` float NOT NULL,
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `escrow` <this shouldn't happen here, since escrow means got transactions.>
--

INSERT INTO `escrow` (`order_id`, `payer_id`, `receiving_id`, `amount`) VALUES
(4000, 1000, 2000, 12.5),
(4001, 1000, 2001, 19);
COMMIT;

--
-- Table structure for table `error`
--
-- insert table structure CODE here
--
-- Dumping data for table `error`
--
-- insert dumping data CODE here

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


