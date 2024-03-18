# Puppet manifest to set up a web server for deployment of web_static

# Ensure nginx package is installed
package { 'nginx':
  ensure => installed,
}

# Define the directories and file content
file { '/data/web_static/releases/test/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
}

file { '/data/web_static/shared/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Hello ALX',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create a symlink to current
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Define nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('module_name/nginx_config.erb'),
  notify  => Service['nginx'],
}

# Manage nginx service
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

